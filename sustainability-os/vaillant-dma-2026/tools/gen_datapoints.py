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
    (Zweckbeschreibung, kein berichtbarer Datenpunkt)
  - existiert bereits ein Objekt mit gleichem `esrs_datapoint` (Verweis), wird es
    NIE überschrieben — bestehende `satisfied_by`-Verknüpfungen bleiben unangetastet
  - frisch erzeugte Objekte starten OHNE `satisfied_by` => emergent ⚠ OFFEN,
    bis ein Mensch die passende KPI/Target verknüpft

Aufruf:
  python3 tools/gen_datapoints.py E1 --version ecdraft2026 --kunde vaillant-dma-2026 --apply
  (ohne --apply: Trockenlauf, zeigt nur den Plan)
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
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def slug(verweis: str) -> str:
    s = verweis.lower()
    for a, b in [("¶", ""), ("(", ""), (")", ""), (".", ""), (" ", "-")]:
        s = s.replace(a, b)
    return re.sub(r"-+", "-", s).strip("-")


def existing_anchors() -> set[str]:
    """Alle bereits vergebenen `esrs_datapoint`-Verweise (für Idempotenz)."""
    anchors = set()
    for p in (ROOT / "objects").glob("datapoint-*.md"):
        m = FM.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        if fm.get("esrs_datapoint"):
            anchors.add(str(fm["esrs_datapoint"]))
    return anchors


def build(std, version, kunde, apply):
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

    have = existing_anchors()
    heute = date.today().isoformat()

    geplant, skip_excl, skip_have, skip_rahmen = [], set(), 0, 0

    for dr in cat["drs"]:
        con = dr.get("concept")
        if con in excluded:
            skip_excl.add(dr["dr_code"])
            continue
        if con not in applicable:
            continue
        topic = TOPIC_MAP.get(con)
        owner = OWNER_MAP.get(con, OWNER_DEFAULT)
        for dp in dr.get("datenpunkte", []):
            if dp.get("datentyp") != "quantitativ":
                continue
            if RAHMEN.match(dp.get("text", "")):
                skip_rahmen += 1
                continue
            verweis = dp["verweis"]
            if verweis in have:
                skip_have += 1
                continue
            oid = f"datapoint-{version}-{slug(verweis)}"
            geplant.append(dict(
                oid=oid, dr=dr["dr_code"], con=con, topic=topic, owner=owner,
                verweis=verweis, text=dp["text"].rstrip(), katalog_dp=dp["id"],
                katalog_version=katalog_version,
            ))

    # --- Ausgabe / Schreiben ---
    print(f"Standard {std} · Katalog {katalog_version} · Kunde {kunde}")
    print(f"  anwendbare Konzepte: {len(applicable)} · ausgeschlossen: {sorted(excluded)}")
    print(f"  übersprungen: {skip_rahmen} Rahmen-Zeilen · {skip_have} bereits vorhanden")
    if skip_excl:
        print(f"  DRs wegen Nicht-Anwendbarkeit übersprungen: {sorted(skip_excl)}")
    print(f"  zu erzeugen: {len(geplant)} quantitative Datenpunkt-Objekte\n")

    by_dr = {}
    for g in geplant:
        by_dr.setdefault(g["dr"], []).append(g)
    for drc in sorted(by_dr):
        print(f"  {drc}: {len(by_dr[drc])} Objekte")

    if not apply:
        print("\n(Trockenlauf — nichts geschrieben. --apply zum Erzeugen.)")
        return

    for g in geplant:
        lines = ["---"]
        lines.append(f"id: {g['oid']}")
        lines.append("type: datapoint")
        lines.append(f"owner: {g['owner']}")
        lines.append("status: offen")
        lines.append(f"stand: {heute}")
        lines.append("vertraulichkeit: intern")
        lines.append(f"esrs_bezug: {std}")
        lines.append("framework: ESRS")
        lines.append(f"katalog_version: {g['katalog_version']}")
        lines.append(f"katalog_dp: {g['katalog_dp']}")
        lines.append(f"esrs_datapoint: \"{g['verweis']}\"")
        lines.append(f"concept: {g['con']}")
        lines.append("datentyp: quantitativ")
        if g["topic"]:
            lines.append(f"concerns: [{g['topic']}]")
        lines.append("satisfied_by: []")
        lines.append("---")
        lines.append(f"# Datenpunkt {g['verweis']} ({g['katalog_version']})")
        lines.append("")
        lines.append(f"Quantitative Offenlegungspflicht (Konzept `{g['con']}`). Originaltext ESRS:")
        lines.append("")
        lines.append(f"> {g['text']}")
        lines.append("")
        lines.append("⚠ **OFFEN** — noch keine KPI/Target verknüpft (`satisfied_by` leer). "
                     "Sobald die passende Kennzahl zugeordnet ist, gilt der Datenpunkt als belegt.")
        lines.append("")
        lines.append("> **Educated Guess** — automatisch aus dem ESRS-Katalog gemintet "
                     "(`tools/gen_datapoints.py`); kein Vaillant-Originaldokument.")
        (ROOT / "objects" / f"{g['oid']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n✓ {len(geplant)} Datenpunkt-Objekte geschrieben nach objects/.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("standard")
    ap.add_argument("--version", required=True, help="z. B. ecdraft2026 oder 2023")
    ap.add_argument("--kunde", required=True)
    ap.add_argument("--apply", action="store_true", help="Objekte schreiben (sonst Trockenlauf)")
    a = ap.parse_args()
    build(a.standard, a.version, a.kunde, a.apply)
