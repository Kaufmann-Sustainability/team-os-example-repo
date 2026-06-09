#!/usr/bin/env python3
"""Visualisiert den Objektgraphen — ohne externe Abhängigkeit (rendert SVG selbst).

Erzeugt:
  diagrams/graph.svg   Programmstruktur als Swimlanes je Thema + Reporting-Kette
  diagrams/graph.mmd   Mermaid-Variante (rendert automatisch auf GitHub)

Aufruf:  python3 tools/graph_viz.py
Benötigt: PyYAML.
"""
from __future__ import annotations
import re, sys, html
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagrams"; OUT.mkdir(exist_ok=True)
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

FARBE = {
    "topic": "#2b6cb0", "iro": "#d69e2e", "target": "#2f855a", "kpi": "#319795",
    "initiative": "#dd6b20", "policy": "#6b46c1", "datapoint": "#718096",
    "disclosure": "#3182ce", "evidence": "#4a5568", "control": "#4a5568",
    "finding": "#e53e3e", "audit-finding": "#c53030", "annual-plan": "#2c7a7b",
}
LANES = ["topic-e1-klima", "topic-e2-umwelt", "topic-e5-kreislauf",
         "topic-s1-belegschaft", "topic-e3-wasser"]
REPORTING = ["datapoint-e1-6-brutto-thg", "disclosure-e1-6-2025", "evidence-inventar-2025",
             "control-thg-bilanzierung", "finding-2026-05-12-spend-based-overcount",
             "audit-finding-2026-baseline-konsistenz"]


def load():
    objs = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if m:
            d = yaml.safe_load(m.group(1)) or {}
            objs[d.get("id", p.stem)] = d
    return objs


def short(oid):
    return oid.split("-", 1)[1] if "-" in oid else oid


def lst(o, k):
    v = o.get(k, [])
    return v if isinstance(v, list) else [v]


def children(objs, tid):
    o = objs[tid]
    out = []
    out += [(i, "iro") for i in lst(o, "has_iro")]
    out += [(p["id"], "policy") for p in objs.values()
            if p.get("type") == "policy" and tid in lst(p, "concerns")]
    out += [(t, "target") for t in lst(o, "has_target")]
    out += [(k, "kpi") for k in lst(o, "has_kpi")]
    out += [(i, "initiative") for i in lst(o, "has_initiative")]
    return [(i, t) for i, t in out if i in objs]


# ---------------- SVG ----------------
def svg(objs):
    LW, CW, CH, GAP = 270, 244, 26, 6           # lane/card Maße
    x0, ytop = 20, 96
    pos = {}                                     # id -> (cx, cy) für Kanten
    body, max_y = [], ytop

    for li, tid in enumerate(LANES):
        lx = x0 + li * LW
        t = objs[tid]
        material = str(t.get("status")) == "wesentlich"
        head = FARBE["topic"] if material else "#a0aec0"
        body.append(f'<rect x="{lx}" y="{ytop}" width="{CW}" height="34" rx="6" fill="{head}"/>')
        body.append(f'<text x="{lx+CW/2}" y="{ytop+22}" text-anchor="middle" '
                    f'fill="white" font-weight="bold" font-size="13">'
                    f'{html.escape(t.get("esrs_bezug",""))} · {html.escape(short(tid))}</text>')
        pos[tid] = (lx + CW / 2, ytop + 17)
        y = ytop + 34 + GAP + 6
        for cid, ctyp in children(objs, tid):
            c = objs[cid]
            label = short(cid)
            if ctyp == "target":
                label += f"  ({c.get('baseline_wert')}→{c.get('zielwert')})"
            col = FARBE.get(ctyp, "#718096")
            body.append(f'<rect x="{lx+10}" y="{y}" width="{CW-20}" height="{CH}" rx="4" '
                        f'fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="1.3"/>')
            body.append(f'<text x="{lx+18}" y="{y+17}" font-size="10.5" fill="#1a202c">'
                        f'{html.escape(label[:34])}</text>')
            pos[cid] = (lx + CW / 2, y + CH / 2)
            y += CH + GAP
        max_y = max(max_y, y)

    # Reporting & Assurance Band
    band_y = max_y + 42
    body.append(f'<text x="{x0}" y="{band_y-10}" font-size="13" font-weight="bold" '
                f'fill="#2d3748">Reporting &amp; Assurance (E1-6)</text>')
    rw = 224
    for ri, rid in enumerate(REPORTING):
        if rid not in objs:
            continue
        rx = x0 + ri * (rw + 14)
        col = FARBE.get(objs[rid].get("type"), "#718096")
        body.append(f'<rect x="{rx}" y="{band_y}" width="{rw}" height="{CH+2}" rx="4" '
                    f'fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="1.3"/>')
        body.append(f'<text x="{rx+10}" y="{band_y+18}" font-size="10.5" fill="#1a202c">'
                    f'{html.escape(short(rid)[:30])}</text>')
        pos[rid] = (rx + rw / 2, band_y + CH / 2)

    # Narrativ-Kanten: "eine Tatsache, drei Aufgaben"
    edges = [
        ("finding-2026-05-12-spend-based-overcount", "kpi-scope3-intensitaet", "#e53e3e", "berührt"),
        ("finding-2026-05-12-spend-based-overcount", "disclosure-e1-6-2025", "#e53e3e", ""),
        ("audit-finding-2026-baseline-konsistenz", "disclosure-e1-6-2025", "#c53030", "challenges"),
        ("disclosure-e1-6-2025", "datapoint-e1-6-brutto-thg", "#3182ce", "discloses"),
    ]
    ed = []
    for a, b, col, lab in edges:
        if a in pos and b in pos:
            (ax, ay), (bx, by) = pos[a], pos[b]
            ed.append(f'<path d="M{ax},{ay} C{ax},{(ay+by)/2} {bx},{(ay+by)/2} {bx},{by}" '
                      f'fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="5,4" '
                      f'marker-end="url(#arr)"/>')
            if lab:
                ed.append(f'<text x="{(ax+bx)/2}" y="{(ay+by)/2-3}" font-size="9" '
                          f'fill="{col}" text-anchor="middle">{lab}</text>')

    # Legende
    leg_y = band_y + CH + 48
    leg = [f'<text x="{x0}" y="{leg_y-8}" font-size="12" font-weight="bold" fill="#2d3748">Legende (Objekt-Typ)</text>']
    for i, (typ, col) in enumerate(FARBE.items()):
        lx = x0 + (i % 7) * 185
        ly = leg_y + (i // 7) * 22
        leg.append(f'<rect x="{lx}" y="{ly}" width="14" height="14" rx="3" fill="{col}" fill-opacity="0.25" stroke="{col}"/>')
        leg.append(f'<text x="{lx+20}" y="{ly+12}" font-size="11" fill="#2d3748">{typ}</text>')

    W = max(x0 + len(LANES) * LW + 10, x0 + len(REPORTING) * (rw + 14) + 10)
    H = leg_y + 60
    n_obj = len(objs)
    n_edge = sum(len(lst(o, k)) for o in objs.values()
                 for k in ("has_target","has_kpi","has_initiative","has_iro","measured_by",
                 "supported_by","approved_by","decided_by","supports","affects","at_risk_from",
                 "has_budget","uses_factor","concerns","informed_by","scored_under","based_on",
                 "applies","discloses","reports","backs","covers","challenges","plans"))
    head = (f'<text x="{x0}" y="34" font-size="20" font-weight="bold" fill="#1a202c">'
            f'Nordmark Sustainability OS — Objektgraph</text>'
            f'<text x="{x0}" y="58" font-size="12" fill="#4a5568">Programmstruktur je '
            f'wesentlichem Thema · {n_obj} Objekte, {n_edge} Kanten · Stand 2026-06-09</text>')
    defs = ('<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="3" '
            'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="#888"/></marker></defs>')
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'font-family="Helvetica,Arial,sans-serif" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>{defs}{head}'
           + "".join(body) + "".join(ed) + "".join(leg) + "</svg>")
    (OUT / "graph.svg").write_text(out, encoding="utf-8")
    return n_obj, n_edge


# ---------------- Mermaid ----------------
def mermaid(objs):
    lines = ["```mermaid", "graph LR"]
    for tid in LANES:
        t = objs[tid]
        lines.append(f'  subgraph {t.get("esrs_bezug")}["{t.get("esrs_bezug")} {short(tid)}"]')
        for cid, _ in children(objs, tid):
            lines.append(f'    {cid.replace("-","_")}["{short(cid)}"]')
        lines.append("  end")
    for tid in LANES:
        for cid, _ in children(objs, tid):
            lines.append(f'  {tid.replace("-","_")} --> {cid.replace("-","_")}')
    # Narrativ
    lines += [
        '  finding_2026_05_12_spend_based_overcount -.berührt.-> kpi_scope3_intensitaet',
        '  finding_2026_05_12_spend_based_overcount -.blockiert.-> disclosure_e1_6_2025',
        '  audit_finding_2026_baseline_konsistenz -.challenges.-> disclosure_e1_6_2025',
        "```",
    ]
    (OUT / "graph.mmd").write_text("# Objektgraph (Mermaid)\n\n" + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    objs = load()
    n_obj, n_edge = svg(objs)
    mermaid(objs)
    print(f"Gerendert: diagrams/graph.svg + graph.mmd  ({n_obj} Objekte, {n_edge} Kanten)")


if __name__ == "__main__":
    main()
