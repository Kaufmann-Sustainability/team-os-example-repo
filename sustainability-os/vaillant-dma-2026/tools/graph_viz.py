#!/usr/bin/env python3
"""Visualisiert den Vaillant-DMA-Graphen als SVG (ohne externe Abhängigkeit).

Lanes = ESRS-Standards. Karten = Themen, gefärbt nach Wesentlichkeit, mit IRO-Anzahl
(Dichte über Füllintensität). Erzeugt diagrams/graph.svg.

Aufruf:  python3 tools/graph_viz.py   ·  benötigt PyYAML.
"""
from __future__ import annotations
import re, sys, html
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "diagrams"; OUT.mkdir(exist_ok=True)
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
STD_ORDER = ["E1", "E2", "E3", "E4", "E5", "ES", "G1", "S1", "S2", "S3", "S4"]
GREEN, GREY = "#2f855a", "#a0aec0"


def load():
    objs = {}
    for p in (ROOT / "objects").glob("*.md"):
        m = FM.search(p.read_text(encoding="utf-8"))
        if m:
            d = yaml.safe_load(m.group(1)) or {}
            d["_body"] = p.read_text(encoding="utf-8")
            objs[d.get("id", p.stem)] = d
    return objs


def main():
    objs = load()
    topics = [o for o in objs.values() if o.get("type") == "topic"]
    iros = [o for o in objs.values() if o.get("type") == "iro"]
    # je Standard: Themen + materielle IRO-Zahl
    by_std = {s: [] for s in STD_ORDER}
    for t in topics:
        s = str(t.get("esrs_bezug"))
        h = re.search(r"# Thema:\s*(.+)", t["_body"])
        t["_label"] = (h.group(1).strip() if h else t["id"])[:18]
        t["_n"] = len(t.get("has_iro", []) if isinstance(t.get("has_iro"), list) else [])
        by_std.setdefault(s, []).append(t)
    mat_iro = {s: 0 for s in by_std}
    for i in iros:
        if str(i.get("wesentlich")).strip('"').lower() == "ja":
            mat_iro[str(i.get("esrs_bezug"))] = mat_iro.get(str(i.get("esrs_bezug")), 0) + 1

    x0, ytop, LW, CH, GAP, HH = 16, 92, 132, 21, 3, 50
    body, max_rows = [], 0
    lanes = [s for s in STD_ORDER if by_std.get(s)]
    for li, s in enumerate(lanes):
        lx = x0 + li * LW
        ths = sorted(by_std[s], key=lambda t: (t.get("status") != "wesentlich", -t["_n"]))
        body.append(f'<rect x="{lx}" y="{ytop}" width="{LW-8}" height="{HH}" rx="6" fill="#2b6cb0"/>')
        body.append(f'<text x="{lx+(LW-8)/2}" y="{ytop+20}" text-anchor="middle" fill="white" '
                    f'font-weight="bold" font-size="15">{s}</text>')
        body.append(f'<text x="{lx+(LW-8)/2}" y="{ytop+38}" text-anchor="middle" fill="#e2e8f0" '
                    f'font-size="9.5">{len(ths)} Th · {mat_iro.get(s,0)} IRO</text>')
        y = ytop + HH + 8
        for t in ths:
            mat = t.get("status") == "wesentlich"
            col = GREEN if mat else GREY
            op = 0.16 + min(t["_n"], 8) / 8 * 0.5     # Dichte über Füllintensität
            body.append(f'<rect x="{lx}" y="{y}" width="{LW-8}" height="{CH}" rx="3" '
                        f'fill="{col}" fill-opacity="{op:.2f}" stroke="{col}" stroke-width="1.1"/>')
            body.append(f'<text x="{lx+5}" y="{y+9}" font-size="7.6" fill="#1a202c">'
                        f'{html.escape(t["_label"])}</text>')
            body.append(f'<text x="{lx+5}" y="{y+18}" font-size="7" fill="#4a5568">'
                        f'{t["_n"]} IRO{"" if t["_n"]==1 else "s"}</text>')
            y += CH + GAP
        max_rows = max(max_rows, len(ths))

    H = ytop + HH + 8 + max_rows * (CH + GAP) + 70
    W = x0 + len(lanes) * LW + 8
    n_t = len(topics); n_tm = sum(1 for t in topics if t.get("status") == "wesentlich")
    n_i = len(iros); n_im = sum(1 for i in iros if str(i.get("wesentlich")).strip('"').lower() == "ja")
    head = (f'<text x="{x0}" y="32" font-size="20" font-weight="bold" fill="#1a202c">'
            f'Vaillant DMA 2026 — Themen je ESRS-Standard</text>'
            f'<text x="{x0}" y="56" font-size="12" fill="#4a5568">'
            f'{n_i} IROs ({n_im} wesentlich) in {n_t} Themen ({n_tm} wesentlich) · '
            f'Kartenfüllung = IRO-Dichte · grün = wesentlich, grau = nicht wesentlich</text>')
    ly = H - 44
    leg = (f'<rect x="{x0}" y="{ly}" width="16" height="14" rx="3" fill="{GREEN}" fill-opacity="0.5" stroke="{GREEN}"/>'
           f'<text x="{x0+22}" y="{ly+12}" font-size="12" fill="#2d3748">wesentliches Thema</text>'
           f'<rect x="{x0+190}" y="{ly}" width="16" height="14" rx="3" fill="{GREY}" fill-opacity="0.5" stroke="{GREY}"/>'
           f'<text x="{x0+212}" y="{ly+12}" font-size="12" fill="#2d3748">nicht wesentlich (Ausschluss-Begründung)</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'font-family="Helvetica,Arial,sans-serif" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>{head}' + "".join(body) + leg + "</svg>")
    (OUT / "graph.svg").write_text(svg, encoding="utf-8")
    print(f"Gerendert: diagrams/graph.svg  ({n_t} Themen, {n_i} IROs)")


if __name__ == "__main__":
    main()
