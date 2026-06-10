#!/usr/bin/env python3
"""
Datenpunkt-Objekt-Generator (ESRS) — KATALOG -> OBJEKTGRAPH.

Schließt die Lücke zwischen den beiden Bedeutungen von "Datenpunkt":
  - KATALOG-Datenpunkt : ESRS-eigenes Wording, absatzweise je DR
                         (reference/esrs-catalog-*.yaml, read-only Referenz).
  - OBJEKT-Datenpunkt  : unser `type: datapoint` im Graphen (objects/datapoint-*.md),
                         der die Pflicht mit internem Inhalt (`satisfied_by`) verbindet.

Bisher waren Objekt-Datenpunkte HANDARBEIT (wenige, grob auf DR-Ebene). Dieser
Generator mintet sie deterministisch aus dem Katalog — aber NUR für QUANTITATIVE
Datenpunkte. Narrative Pflichten bleiben bewusst auf DR-Ebene (der Berichts-Entwurf
deckt sie konzept-weit ab); sie zu vereinzeln brächte nur leere Prosa-Stubs.

Regeln (deterministisch, kein LLM, idempotent):
  - nur DRs, deren `concept` für den Kunden ANWENDBAR ist (Ausschlüsse übersprungen)
  - nur Katalog-Datenpunkte mit `datentyp: quantitativ`
  - die DR-Rahmen-Zeile ("The objective of this DR ...") wird übersprungen
  - frisch erzeugte Objekte starten OHNE `satisfied_by` => emergent ⚠ OFFEN
  - bestehende handgemachte Datenpunkt-Objekte (ohne `katalog_dp`) werden NIE angefasst

Zwei Modi:
  - Standard : erzeugt nur FEHLENDE Objekte; vorhandene bleiben unangetastet.
  - --refresh: zieht den Katalogtext in bereits generierte Objekte nach (z. B. nach
               einem Katalog-Reimport), bewahrt dabei aber `satisfied_by` + `status`
               (die menschliche Verknüpfungs-Arbeit). Handgemachte Objekte bleiben tabu.

Aufruf:
  python3 tools/gen_datapoints.py E1 --version ecdraft2026 --kunde vaillant-dma-2026 --apply
  python3 tools/gen_datapoints.py E1 --version ecdraft2026 --kunde vaillant-dma-2026 --refresh --apply
Benötigt: PyYAML.
"""
from __future__ import annotations
import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

# Konzept -> Thema (für die `concerns`-Kante). Fehlt ein Mapping, wird `concerns`
# weggelassen — das Objekt bleibt über `concept` verankert und valide.
TOPIC_MAP = {
    "energy": "topic-e1-energie",
    "gross-ghg": "topic-e1-klimawandel-mitigation",
    "removals-credits": "topic-e1-klimawandel-mitigation",
    "financial-effects": "topic-e1-klimawandel-adaptation",
}
# Konzept -> fachlicher Owner (person-id). Default, falls Konzept nicht gelistet.
OWNER_MAP = {
    "energy": "person-vaillant-decarb",
    "gross-ghg": "person-vaillant-decarb",
    "removals-credits": "person-vaillant-decarb",
    "financial-effects": "person-vaillant-cfo",
}
OWNER_DEFAULT = "person-vaillant-decarb"

# Rahmen-Zeilen, die zwar als quantitativ markiert sind, aber keine berichtbare
# Kennzahl tragen (Zweckbeschreibung jedes DR).
RAHMEN = re.compile(r"^\s*\d+\.\s+The objective of this DR", re.IGNORECASE)


def slug(verweis: str) -> str:
    s = verweis.lower()
    for a, b in [("¶", ""), ("(", ""), (")", ""), (".", ""), (" ", "-")]:
        s = s.replace(a, b)
    return re.sub(r"-+", "-", s).strip("-")


def read_fm(path: Path) -> dict:
    m = FM.search(path.read_text(encoding="utf-8"))
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def render(g: dict, sat: list, status: str, heute: str) -> str:
    """Deterministische Datei-Repräsentation; Body spiegelt den Verknüpfungs-Stand."""
    L = ["---",
         f"id: {g['oid']}",
         "type: datapoint",
         f"owner: {g['owner']}",
         f"status: {status}",
         f"stand: {heute}",
         "vertraulichkeit: intern",
         f"esrs_bezug: {g['std']}",
         "framework: ESRS",
         f"katalog_version: {g['katalog_version']}",
         f"katalog_dp: {g['katalog_dp']}",
         f"esrs_datapoint: \"{g['verweis']}\"",
         f"concept: {g['con']}",
         "datentyp: quantitativ"]
    if g["topic"]:
        L.append(f"concerns: [{g['topic']}]")
    if sat:
        L.append(f"satisfied_by: [{', '.join(sat)}]")
    else:
        L.append("satisfied_by: []")
    L += ["---",
          f"# Datenpunkt {g['verweis']} ({g['katalog_version']})",
          "",
          f"Quantitative Offenlegungspflicht (Konzept `{g['con']}`). Originaltext ESRS:",
          "",
          f"> {g['text']}",
          ""]
    if sat:
        quellen = ", ".join(f"`{s}`" for s in sat)
        L.append(f"✅ **BELEGT** — verknüpft mit {quellen} über `satisfied_by`.")
    else:
        L.append("⚠ **OFFEN** — noch keine KPI/Target verknüpft (`satisfied_by` leer). "
                 "Sobald die passende Kennzahl zugeordnet ist, gilt der Datenpunkt als belegt.")
    L += ["",
          "> **Educated Guess** — automatisch aus dem ESRS-Katalog gemintet "
          "(`tools/gen_datapoints.py`); kein Vaillant-Originaldokument."]
    return "\n".join(L) + "\n"


def build(std, version, kunde, apply, refresh):
    catf = ROOT / "reference" / f"esrs-catalog-{std.lower()}-{version}.yaml"
    if not catf.exists():
        sys.exit(f"Kein Katalog: {catf.name}")
    cat = yaml.safe_load(catf.read_text(encoding="utf-8"))
    katalog_version = cat.get("katalog_version", version)

    appl = yaml.safe_load(
        (ROOT / "reference" / f"anwendbarkeit-{kunde}-{std.lower()}.yaml").read_text(encoding="utf-8")
    )
    applicable = {a["konzept"] for a in appl.get("anwendbar", [])}
    excluded = {e["konzept"] for e in appl.get("nicht_anwendbar", [])}
    heute = date.today().isoformat()

    create, refr, skip_have, skip_hand, skip_rahmen, skip_excl = [], [], 0, 0, 0, set()

    for dr in cat["drs"]:
        con = dr.get("concept")
        if con in excluded:
            skip_excl.add(dr["dr_code"]); continue
        if con not in applicable:
            continue
        for dp in dr.get("datenpunkte", []):
            if dp.get("datentyp") != "quantitativ":
                continue
            if RAHMEN.match(dp.get("text", "")):
                skip_rahmen += 1; continue
            g = dict(
                oid=f"datapoint-{version}-{slug(dp['verweis'])}", std=std,
                dr=dr["dr_code"], con=con, topic=TOPIC_MAP.get(con),
                owner=OWNER_MAP.get(con, OWNER_DEFAULT), verweis=dp["verweis"],
                text=dp["text"].rstrip(), katalog_dp=dp["id"], katalog_version=katalog_version,
            )
            path = ROOT / "objects" / f"{g['oid']}.md"
            if path.exists():
                fm_old = read_fm(path)
                if "katalog_dp" not in fm_old:        # handgemacht -> niemals anfassen
                    skip_hand += 1
                elif refresh:                          # generiert -> Text nachziehen, Links bewahren
                    refr.append((g, list(fm_old.get("satisfied_by") or []),
                                 fm_old.get("status", "offen")))
                else:
                    skip_have += 1
            else:
                create.append(g)

    print(f"Standard {std} · Katalog {katalog_version} · Kunde {kunde} · Modus "
          f"{'REFRESH' if refresh else 'CREATE'}")
    print(f"  anwendbare Konzepte: {len(applicable)} · ausgeschlossen: {sorted(excluded)}")
    print(f"  übersprungen: {skip_rahmen} Rahmen-Zeilen · {skip_hand} handgemacht"
          + ("" if refresh else f" · {skip_have} bereits vorhanden"))
    if skip_excl:
        print(f"  DRs wegen Nicht-Anwendbarkeit übersprungen: {sorted(skip_excl)}")
    print(f"  NEU zu erzeugen: {len(create)}" + (f" · zu AKTUALISIEREN: {len(refr)}" if refresh else ""))

    if not apply:
        print("\n(Trockenlauf — nichts geschrieben. --apply zum Schreiben.)")
        return

    for g in create:
        (ROOT / "objects" / f"{g['oid']}.md").write_text(render(g, [], "offen", heute), encoding="utf-8")
    for g, sat, status in refr:
        (ROOT / "objects" / f"{g['oid']}.md").write_text(render(g, sat, status, heute), encoding="utf-8")

    print(f"\n✓ {len(create)} erzeugt" + (f", {len(refr)} aktualisiert" if refresh else "")
          + " in objects/.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("standard")
    ap.add_argument("--version", required=True, help="z. B. ecdraft2026 oder 2023")
    ap.add_argument("--kunde", required=True)
    ap.add_argument("--apply", action="store_true", help="schreiben (sonst Trockenlauf)")
    ap.add_argument("--refresh", action="store_true",
                    help="Katalogtext in bestehende generierte Objekte nachziehen (Links bleiben)")
    a = ap.parse_args()
    build(a.standard, a.version, a.kunde, a.apply, a.refresh)
