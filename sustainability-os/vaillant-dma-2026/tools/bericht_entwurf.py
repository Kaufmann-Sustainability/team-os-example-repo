#!/usr/bin/env python3
"""
Bericht-Entwurfs-Generator (ESRS).

Konsumiert die drei Schichten und erzeugt einen Markdown-ENTWURF je anwendbarem
Datenpunkt:
  1. Katalog        reference/esrs-catalog-<std>-*.yaml   (geteilt, alle Datenpunkte)
  2. Anwendbarkeit  reference/anwendbarkeit-<kunde>-<std>.yaml (kundenspezifisch, DMA-Output)
  3. Inhalt         objects/datapoint-*.md  ->  satisfied_by-Kanten auf Targets/KPIs/...

Die Lücke wird EMERGENT sichtbar: jeder anwendbare Absatz ohne verknüpften Inhalt
erhält einen ⚠ OFFEN-Marker. Der Generator urteilt NICHT über inhaltliche
Vollständigkeit (z. B. ob alle signifikanten Scope-3-Kategorien abgedeckt sind) —
das ist ein Review-/disclosure-readiness-Schritt durch den Menschen.

Aufruf:
  python3 tools/bericht_entwurf.py E1 --kunde vaillant-dma-2026 --out reporting/bericht-entwurf-e1.md
Benötigt: PyYAML.
"""
from __future__ import annotations
import argparse, glob, re, sys
from datetime import date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---(.*)$", re.DOTALL)
H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def load_objects():
    """id -> (frontmatter-dict, titel)"""
    out = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        t = H1.search(m.group(2))
        out[fm.get("id", p.stem)] = (fm, t.group(1).strip() if t else "")
    return out


def run(std, kunde, out_path):
    cat_files = sorted(glob.glob(str(ROOT / "reference" / f"esrs-catalog-{std.lower()}-*.yaml")))
    if not cat_files:
        sys.exit(f"Kein Katalog für {std} gefunden.")
    cat = yaml.safe_load(open(cat_files[0]))
    appl = yaml.safe_load(open(ROOT / "reference" / f"anwendbarkeit-{kunde}-{std.lower()}.yaml"))
    objs = load_objects()

    applicable = {a["dr"]: a["grund"] for a in appl.get("anwendbar", [])}
    excluded = appl.get("nicht_anwendbar", [])

    # datapoint-Objekte je dr_code (Inhalts-Mapping, validiert via satisfied_by)
    by_dr = {}
    for oid, (fm, _t) in objs.items():
        if fm.get("type") == "datapoint" and fm.get("framework") == "ESRS" and fm.get("dr_code"):
            by_dr.setdefault(fm["dr_code"], []).append(fm)

    L = []
    w = L.append
    w(f"# Berichts-Entwurf — ESRS {std}")
    w(f"\n> **MASCHINENGENERIERTER ROH-ENTWURF — nicht freigegeben.** Erzeugt {date.today()} "
      f"via `tools/bericht_entwurf.py`. Kunde: `{kunde}`. Katalog: `{cat.get('katalog_version')}`.")
    w(f">\n> Inhaltliche Vollständigkeit je Absatz (z. B. ob Scope-3-Ziele *alle signifikanten "
      f"Kategorien* abdecken) ist **fachlich im Review zu prüfen** — der Generator markiert nur, "
      f"wo *kein* Inhalt verknüpft ist.\n")

    # Kennzahlen
    total_dp = mapped_dr = open_dr = 0
    for dr in cat["drs"]:
        if dr["dr_code"] not in applicable:
            continue
        total_dp += len(dr["datenpunkte"])
        if by_dr.get(dr["dr_code"]):
            mapped_dr += 1
        else:
            open_dr += 1
    w(f"**Stand:** {len(applicable)} anwendbare DRs ({total_dp} Datenpunkte) · "
      f"{mapped_dr} mit verknüpftem Inhalt · {open_dr} vollständig offen · "
      f"{len(excluded)} DR ausgeschlossen.\n")

    for dr in cat["drs"]:
        code = dr["dr_code"]
        if code not in applicable:
            continue
        dps = by_dr.get(code, [])
        sources = []
        for fm in dps:
            for sid in fm.get("satisfied_by", []) or []:
                title = objs.get(sid, ({}, ""))[1] or sid
                sources.append((sid, title))
        mark = "✅ Inhalt verknüpft" if sources else "⚠ OFFEN — kein Inhalt verknüpft"
        w(f"\n---\n\n## {code} — {dr['dr_name']}  ·  {mark}")
        w(f"\n*Anwendbar, weil:* {applicable[code]}")
        if sources:
            w(f"\n**Verknüpfte Quellen (`satisfied_by`):**")
            for sid, title in sources:
                w(f"- `{sid}` — {title}")
        w("")
        for dp in dr["datenpunkte"]:
            w(f"\n**{dp['verweis']}**  _({dp['datentyp']})_")
            w(f"> {dp['text'].rstrip()}")
            if sources:
                w(f"\n_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**")
            else:
                w(f"\n⚠ **OFFEN** — kein `datapoint`-Objekt/Inhalt für {code} verknüpft.")

    if excluded:
        w("\n---\n\n## Nicht anwendbar (Ausschlüsse — prüfungsrelevant)")
        for e in excluded:
            w(f"- **{e['dr']}** — {e['grund']}")

    Path(out_path).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"✓ Entwurf: {len(applicable)} DRs, {total_dp} Datenpunkte, "
          f"{open_dr} offene DRs -> {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("standard")
    ap.add_argument("--kunde", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.standard, a.kunde, a.out)
