#!/usr/bin/env python3
"""
Bericht-Entwurfs-Generator (ESRS) — VERSIONS-PARAMETRIERT.

Erzeugt einen Markdown-Entwurf je anwendbarem Datenpunkt, ausspielbar gegen JEDE
Katalog-Version (z. B. ESRS 2023 final ODER EC-Entwurf 2026). Inhalt ist nicht an
DR-Nummern gebunden, sondern an stabile KONZEPTE (reference/esrs-concepts.yaml);
jede Katalog-Version bildet ihre DR-Codes via `concept:` darauf ab. -> Ein Mapping,
alle Versionen.

Zwei Zuordnungs-Quellen je Konzept:
  - MANUELL    : datapoint-*-Objekte mit `satisfied_by` (autoritativ).
  - ABGELEITET : Tier-1-Regeln type->Konzept, topologie-gegated (deterministisch, kein
                 LLM, nicht halluzinierbar). KPIs & narrative DRs werden NICHT abgeleitet.

Lücke bleibt emergent: anwendbarer DR ohne Inhalt -> ⚠ OFFEN. Inhaltliche
Vollständigkeit je Absatz ist ein menschlicher Review-Schritt.

Aufruf:
  python3 tools/bericht_entwurf.py E1 --version 2023        --kunde vaillant-dma-2026
  python3 tools/bericht_entwurf.py E1 --version ecdraft2026 --kunde vaillant-dma-2026
Benötigt: PyYAML.
"""
from __future__ import annotations
import argparse, re, sys
from datetime import date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---(.*)$", re.DOTALL)
H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def load_objects():
    out = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        t = H1.search(m.group(2))
        out[fm.get("id", p.stem)] = (fm, t.group(1).strip() if t else "")
    return out


def cat_path(std, version):
    p = ROOT / "reference" / f"esrs-catalog-{std.lower()}-{version}.yaml"
    if not p.exists():
        sys.exit(f"Kein Katalog: {p.name}")
    return p


def load_spine(std):
    # Sucht unter reference/esrs-concepts*.yaml die Spine, deren `standard` == std ist.
    # E1 liegt in esrs-concepts.yaml, weitere Standards in esrs-concepts-<std>.yaml.
    for p in sorted((ROOT / "reference").glob("esrs-concepts*.yaml")):
        sp = yaml.safe_load(open(p))
        if sp.get("standard") == std:
            return sp
    sys.exit(f"Keine Konzept-Spine für {std}")


def run(std, version, kunde, out_path):
    cat = yaml.safe_load(open(cat_path(std, version)))
    spine = load_spine(std)
    rules = [(r["typ"], r["feld"], r["praefix"], r["konzept"]) for r in spine.get("ableitung", [])]
    objs = load_objects()
    appl = yaml.safe_load(open(ROOT / "reference" / f"anwendbarkeit-{kunde}-{std.lower()}.yaml"))

    # Anwendbarkeit ist bereits konzept-nativ (versionsunabhängig)
    appl_con = {a["konzept"]: a["grund"] for a in appl.get("anwendbar", [])}
    excl_con = {e["konzept"]: e["grund"] for e in appl.get("nicht_anwendbar", [])}

    # --- Zuordnung je Konzept aufbauen ---
    # MANUELL: datapoint.satisfied_by -> Konzept DIREKT (versionsunabhängig, kein dr_code)
    manual = {}   # concept -> set(ids)
    for oid, (fm, _t) in objs.items():
        if fm.get("type") == "datapoint" and fm.get("satisfied_by"):
            con = fm.get("concept")
            if con:
                manual.setdefault(con, set()).update(fm["satisfied_by"])
    # ABGELEITET: type + Topologie-Gate -> Konzept
    derived = {}  # concept -> list[(id, rule)]
    for oid, (fm, _t) in objs.items():
        for typ, feld, praefix, con in rules:
            if fm.get("type") == typ and any(str(x).startswith(praefix) for x in fm.get(feld, []) or []):
                derived.setdefault(con, []).append((oid, f"type={typ} ∧ {feld}->{praefix}-*"))
                break

    def title(i):
        return objs.get(i, ({}, ""))[1] or i

    L, w = [], None
    w = L.append
    w(f"# Berichts-Entwurf — ESRS {std}  ·  Fassung `{cat.get('katalog_version')}`")
    w(f"\n> **MASCHINENGENERIERTER ROH-ENTWURF — nicht freigegeben.** Erzeugt {date.today()} "
      f"via `tools/bericht_entwurf.py --version {version}`. Kunde: `{kunde}`.")
    w(f">\n> Inhalt ist über **stabile Konzepte** zugeordnet (versionsunabhängig); diese Fassung "
      f"nummeriert sie als `{cat.get('katalog_version')}`. Quellen sind als **(manuell)** "
      f"[autoritativ] oder **(abgeleitet)** [Tier-1-Regel, deterministisch] markiert. "
      f"Inhaltliche Vollständigkeit je Absatz ist im Review zu prüfen.\n")

    n_appl = n_map = n_open = 0
    for dr in cat["drs"]:
        con = dr.get("concept")
        if con not in appl_con:
            continue
        n_appl += 1
        man = sorted(manual.get(con, set()))
        der = derived.get(con, [])
        if man or der:
            n_map += 1
        else:
            n_open += 1

    w(f"**Stand:** {n_appl} anwendbare DRs · {n_map} mit Inhalt · {n_open} offen · "
      f"{sum(1 for d in cat['drs'] if d.get('concept') in excl_con)} ausgeschlossen.\n")

    for dr in cat["drs"]:
        con = dr.get("concept")
        if con not in appl_con:
            continue
        man = sorted(manual.get(con, set()))
        der = derived.get(con, [])
        mark = "✅ Inhalt zugeordnet" if (man or der) else "⚠ OFFEN — kein Inhalt zugeordnet"
        w(f"\n---\n\n## {dr['dr_code']} — {dr['dr_name']}  ·  {mark}")
        w(f"\n*Konzept:* `{con}`  ·  *anwendbar, weil:* {appl_con[con]}")
        if man:
            w(f"\n**Quellen (manuell · `satisfied_by`):**")
            for i in man:
                w(f"- `{i}` — {title(i)}")
        if der:
            w(f"\n**Quellen (abgeleitet · Tier-1-Regel):**")
            for i, rule in der:
                w(f"- `{i}` — {title(i)}  _({rule})_")
        w("")
        for dp in dr["datenpunkte"]:
            w(f"\n**{dp['verweis']}**  _({dp.get('datentyp','')})_")
            w(f"> {dp['text'].rstrip()}")
            if man or der:
                w(f"\n_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**")
            else:
                w(f"\n⚠ **OFFEN** — kein Inhalt für Konzept `{con}` zugeordnet.")

    excl = [d for d in cat["drs"] if d.get("concept") in excl_con]
    if excl:
        w("\n---\n\n## Nicht anwendbar (Ausschlüsse — prüfungsrelevant)")
        for d in excl:
            w(f"- **{d['dr_code']}** ({d.get('concept')}) — {excl_con[d.get('concept')]}")

    Path(out_path).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ {cat.get('katalog_version'):>14}: {n_appl} DRs · {n_map} mit Inhalt · "
          f"{n_open} offen -> {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("standard")
    ap.add_argument("--version", required=True, help="z. B. 2023 oder ecdraft2026")
    ap.add_argument("--kunde", required=True)
    ap.add_argument("--out")
    a = ap.parse_args()
    out = a.out or f"reporting/bericht-entwurf-{a.standard.lower()}-{a.version}.md"
    run(a.standard, a.version, a.kunde, str(ROOT / out) if not Path(out).is_absolute() else out)
