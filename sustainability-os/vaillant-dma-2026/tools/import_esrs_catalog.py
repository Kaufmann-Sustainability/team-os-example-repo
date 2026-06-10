#!/usr/bin/env python3
"""
ESRS-Datenpunkt-Katalog-Importer.

Liest ein EFRAG-/EC-Datenpunkt-Workbook (xlsx) und erzeugt einen VERSIONIERTEN
Referenz-Katalog (YAML). Der Katalog ist externe Referenzdaten — wie der
Emissionsfaktoren-Katalog —, nicht unternehmensspezifische Artefakte: einmal
importiert, je Standard-Release versioniert.

Aufruf:
  python3 tools/import_esrs_catalog.py reference/esrs-ec-draft-2026.xlsx "ESRS E1" \\
          --version ec-draft-2026 --out reference/esrs-catalog-e1-ecdraft2026.yaml
"""
import argparse, datetime, glob, re
import openpyxl
import yaml
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "reference"

# DRs mit überwiegend quantitativen/monetären Datenpunkten (Heuristik für datentyp)
QUANT_DRS = {"E1-7", "E1-8", "E1-9", "E1-10", "E1-11"}


def restore_co2(t: str) -> str:
    """Stellt das in der Quelle verlorene tiefgestellte ₂ der CO₂-Familie wieder her.
    Die EFRAG-xlsx legt das Subscript inkonsistent ab (mal 'CO2eq', mal 'CO' / 'tCOeq').
    Reihenfolge bewusst: erst die fehlenden Fälle, dann Normalisierung der vorhandenen."""
    t = re.sub(r"\btCOeq\b", "tCO₂eq", t)   # 'tCOeq' / 'tCOeq)' -> tCO₂eq
    t = re.sub(r"\bCOeq\b", "CO₂eq", t)     # 'COeq'  -> CO₂eq
    t = re.sub(r"\bCO\b", "CO₂", t)         # alleinstehendes 'CO' (z. B. 'biogenic CO emissions')
    t = re.sub(r"\bCO2eq\b", "CO₂eq", t)    # vorhandenes 'CO2eq' auf Subscript normalisieren
    t = re.sub(r"\bCO2\b", "CO₂", t)        # vorhandenes 'CO2'
    return t


def concept_map(standard: str, version: str) -> dict:
    """dr_code -> concept aus der passenden Konzept-Spine (reference/esrs-concepts*.yaml).
    Macht das `concept:`-Feld reproduzierbar, statt es nach dem Import von Hand zu setzen."""
    for p in sorted(glob.glob(str(REF / "esrs-concepts*.yaml"))):
        sp = yaml.safe_load(open(p))
        if sp.get("standard") == standard:
            out = {}
            for k in sp.get("konzepte", []):
                code = (k.get("nummerierung") or {}).get(version)
                if code:
                    out[code] = k["id"]
            return out
    return {}


def slug(*parts):
    s = "".join(p for p in parts if p)
    for a, b in [("(", ""), (")", ""), (" ", ""), (".", "")]:
        s = s.replace(a, b)
    return s.lower()


def run(xlsx, sheet, version, out):
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    H = {h: i for i, h in enumerate(rows[0])}
    def g(r, k): v = r[H[k]]; return "" if v is None else str(v).strip()

    standard = sheet.replace("ESRS ", "").strip()
    con_map = concept_map(standard, version)   # dr_code -> concept (aus Spine, reproduzierbar)
    drs = {}          # dr_code -> {name, datapoints:[...]}
    for r in rows[1:]:
        if g(r, "Chapter") != "Disclosure Requirements":
            continue
        code = g(r, "DR Code")
        if not code:
            continue
        dr = drs.setdefault(code, {"name": "", "datapoints": []})
        if g(r, "DR Name") and not dr["name"]:
            dr["name"] = g(r, "DR Name")
        # granularer Datenpunkt = DR-Typ-Zeile mit Absatznummer
        if g(r, "Type") != "DR" or not g(r, "Para #"):
            continue
        para, sub, subsub = g(r, "Para #"), g(r, "Sub-item"), g(r, "Sub-sub-item")
        text = restore_co2(g(r, "Text"))   # volle Länge (keine Kappung) + ₂ wiederhergestellt
        datentyp = "quantitativ" if code in QUANT_DRS else "narrativ"
        dr["datapoints"].append({
            "id": f"dp-{version}-{slug(code, para, sub, subsub)}",
            "verweis": f"{code} ¶{para}{sub}{subsub}".strip(),
            "datentyp": datentyp,
            "text": text,
        })

    # YAML von Hand schreiben (deterministisch, keine Sortier-Überraschungen)
    n_dp = sum(len(d["datapoints"]) for d in drs.values())
    lines = [
        f"# ESRS-Datenpunkt-Katalog — REFERENZ (maschinengeneriert, nicht händisch pflegen)",
        f"# Erzeugt: {datetime.date.today()}  via tools/import_esrs_catalog.py",
        f"standard: {standard}",
        f"katalog_version: {version}",
        f"quelle: {xlsx}",
        f"disclosure_requirements: {len(drs)}",
        f"datenpunkte: {n_dp}",
        "drs:",
    ]
    def dump_str(s):
        return '"' + s.replace('"', "'") + '"'
    for code in sorted(drs, key=lambda x: int(x.split("-")[1])):
        d = drs[code]
        lines.append(f"  - dr_code: {code}")
        lines.append(f"    dr_name: {dump_str(d['name'])}")
        if con_map.get(code):
            lines.append(f"    concept: {con_map[code]}")
        lines.append(f"    datenpunkte:")
        for dp in d["datapoints"]:
            lines.append(f"      - id: {dp['id']}")
            lines.append(f"        verweis: {dump_str(dp['verweis'])}")
            lines.append(f"        datentyp: {dp['datentyp']}")
            lines.append(f"        text: {dump_str(dp['text'])}")
    open(out, "w").write("\n".join(lines) + "\n")
    print(f"✓ {len(drs)} DRs, {n_dp} Datenpunkte -> {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx")
    ap.add_argument("sheet")
    ap.add_argument("--version", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    run(a.xlsx, a.sheet, a.version, a.out)
