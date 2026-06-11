#!/usr/bin/env python3
"""Wegwerf-Preview: rendert dieselben Topic-Graphdaten in drei rotierbaren Layouts
als statische SVG-Schnappschüsse, damit man die Varianten vergleichen kann.
Nicht Teil des Cockpits — dient nur der Entscheidungsfindung."""
import math, html, importlib.util, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("cockpit", ROOT / "tools" / "cockpit.py")
ck = importlib.util.module_from_spec(spec); spec.loader.exec_module(ck)

objs = ck.load()
COL = {"topic": "#e3e8ee", "iro": "#d29922", "target": "#58a6ff", "kpi": "#3fb950",
       "initiative": "#bc8cff", "policy": "#f778ba", "strategy": "#f0883e"}

def raw_short(i, n=22):
    t = (objs[i]["fm"].get("kurztitel") or objs[i]["fm"].get("iro_nr")
         or objs[i]["fm"].get("titel") or i)
    t = str(t)
    return t if len(t) <= n else t[:n - 1] + "…"

def members_of(tid):
    fm = objs[tid]["fm"]
    mem = [tid]
    for f2 in ("has_iro", "has_target", "has_kpi", "has_initiative"):
        mem += (fm.get(f2) or [])
    mem += [o for o, x in objs.items() if x["fm"].get("type") in ("policy", "strategy")
            and tid in (x["fm"].get("concerns") or [])]
    mem = list(dict.fromkeys(m for m in mem if m in objs))
    idx = {m: i for i, m in enumerate(mem)}
    nodes = [{"id": m, "l": raw_short(m), "t": objs[m]["fm"].get("type", "")} for m in mem]
    edges, seen = [], set()
    for m in mem:
        for _f, ids in ck.edges_out(objs[m]["fm"]):
            for t2 in ids:
                if t2 in idx and idx[m] != idx[t2]:
                    k = (min(idx[m], idx[t2]), max(idx[m], idx[t2]))
                    if k not in seen:
                        seen.add(k); edges.append([idx[m], idx[t2]])
    return nodes, edges

# kanten-reichstes Thema wählen
topics = [o for o, x in objs.items() if x["fm"].get("type") == "topic"]
best = max(topics, key=lambda t: len(members_of(t)[1]))
NODES, EDGES = members_of(best)
TITLE = (objs[best]["fm"].get("titel") or best)
print(f"Thema: {best}  ({len(NODES)} Knoten, {len(EDGES)} Kanten)")

W, H = 700, 470
BG = "#0d1117"

def frame(inner, caption):
    return (f"<svg viewBox='0 0 {W} {H}' xmlns='http://www.w3.org/2000/svg' "
            f"font-family='-apple-system,Segoe UI,sans-serif'>"
            f"<rect width='{W}' height='{H}' fill='{BG}' rx='10'/>"
            f"<text x='18' y='28' fill='#e3e8ee' font-size='15' font-weight='600'>{html.escape(caption)}</text>"
            f"<text x='18' y='46' fill='#8a97a6' font-size='11'>{html.escape(TITLE)} — "
            f"{len(NODES)} Objekte · {len(EDGES)} Verknüpfungen</text>"
            f"{inner}</svg>")

def node_circle(sx, sy, t, d, rad):
    c = COL.get(t, "#8a97a6")
    return (f"<circle cx='{sx:.1f}' cy='{sy:.1f}' r='{rad:.1f}' fill='{c}' "
            f"fill-opacity='{0.45 + d * 0.55:.2f}'/>")

def label(sx, sy, txt, d, rad):
    return (f"<text x='{sx + rad + 3:.1f}' y='{sy + 3:.1f}' fill='#e3e8ee' "
            f"fill-opacity='{0.35 + d * 0.5:.2f}' font-size='9.5'>{html.escape(txt)}</text>")

def project(x, y, z, ay, ax, R, cx, cy):
    X = x * math.cos(ay) + z * math.sin(ay)
    Z = -x * math.sin(ay) + z * math.cos(ay)
    Y2 = y * math.cos(ax) - Z * math.sin(ax)
    Z3 = y * math.sin(ax) + Z * math.cos(ax)
    return cx + X * R, cy + Y2 * R, Z3

# ---------------------------------------------------------------- A) Typ-Orbits
def layout_orbits():
    cx, cy, R = W / 2, H / 2 + 18, 150
    ay, ax = 0.7, 0.42
    LAYER = {"topic": -1.15, "iro": -0.78, "policy": -0.78, "strategy": -0.78,
             "target": 0.0, "kpi": 0.82, "initiative": 0.82}
    ring = {"topic": 0.0, "iro": 0.92, "policy": 0.92, "strategy": 0.92,
            "target": 0.78, "kpi": 0.92, "initiative": 0.92}
    by_layer = {}
    for i, n in enumerate(NODES):
        by_layer.setdefault(round(LAYER.get(n["t"], 0.0), 2), []).append(i)
    ang = {}
    # oberer Ring: gleichmäßig
    top = sorted(by_layer.get(-0.78, []), key=lambda i: (NODES[i]["t"], NODES[i]["l"]))
    for k, i in enumerate(top):
        ang[i] = 2 * math.pi * k / max(1, len(top))
    # Barycenter für mittleren & unteren Ring
    nbr = {i: [] for i in range(len(NODES))}
    for a, b in EDGES:
        nbr[a].append(b); nbr[b].append(a)
    def bary(i, known):
        xs = [math.cos(ang[j]) for j in nbr[i] if j in known]
        ys = [math.sin(ang[j]) for j in nbr[i] if j in known]
        return math.atan2(sum(ys), sum(xs)) if xs else None
    mid = by_layer.get(0.0, [])
    for k, i in enumerate(mid):
        a = bary(i, ang); ang[i] = a if a is not None else 2 * math.pi * k / max(1, len(mid))
    bot = by_layer.get(0.82, [])
    for k, i in enumerate(bot):
        a = bary(i, ang); ang[i] = a if a is not None else 2 * math.pi * k / max(1, len(bot))
    for i in by_layer.get(-1.15, []):
        ang[i] = 0.0
    P = []
    for i, n in enumerate(NODES):
        rr = ring.get(n["t"], 0.9); a = ang.get(i, 0.0)
        P.append(project(math.cos(a) * rr, LAYER.get(n["t"], 0.0), math.sin(a) * rr, ay, ax, R, cx, cy))
    out = []
    # Ring-Andeutung
    for ly in (-0.78, 0.0, 0.82):
        pts = [project(math.cos(t / 28 * 2 * math.pi) * (0.92 if ly else 0.78), ly,
                       math.sin(t / 28 * 2 * math.pi) * (0.92 if ly else 0.78), ay, ax, R, cx, cy)
               for t in range(29)]
        d = "M" + " L".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
        out.append(f"<path d='{d}' fill='none' stroke='#30363d' stroke-opacity='0.5'/>")
    for a, b in EDGES:
        pa, pb = P[a], P[b]; d = ((pa[2] + pb[2]) / 2 + 1) / 2
        out.append(f"<line x1='{pa[0]:.1f}' y1='{pa[1]:.1f}' x2='{pb[0]:.1f}' y2='{pb[1]:.1f}' "
                   f"stroke='#7896d7' stroke-opacity='{0.10 + d * 0.4:.2f}'/>")
    for i in sorted(range(len(NODES)), key=lambda j: P[j][2]):
        p = P[i]; d = (p[2] + 1) / 2; rad = 3 + d * 4
        out.append(node_circle(p[0], p[1], NODES[i]["t"], d, rad))
        if NODES[i]["t"] in ("topic", "target"):
            out.append(label(p[0], p[1], NODES[i]["l"], d, rad))
    return frame("".join(out), "A · Typ-Orbits (Ringkette)")

# ---------------------------------------------------------- B) Kraft-Cluster 3D
def layout_force():
    import random; random.seed(7)
    n = len(NODES); pos = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(n)]
    adj = [[] for _ in range(n)]
    for a, b in EDGES:
        adj[a].append(b); adj[b].append(a)
    k = 0.9
    for it in range(420):
        disp = [[0.0, 0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dx = pos[i][0] - pos[j][0]; dy = pos[i][1] - pos[j][1]; dz = pos[i][2] - pos[j][2]
                dist = math.sqrt(dx * dx + dy * dy + dz * dz) or 0.01
                f = k * k / dist / dist
                ux, uy, uz = dx / dist, dy / dist, dz / dist
                disp[i][0] += ux * f; disp[i][1] += uy * f; disp[i][2] += uz * f
                disp[j][0] -= ux * f; disp[j][1] -= uy * f; disp[j][2] -= uz * f
        for a, b in EDGES:
            dx = pos[a][0] - pos[b][0]; dy = pos[a][1] - pos[b][1]; dz = pos[a][2] - pos[b][2]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz) or 0.01
            f = dist * dist / k
            ux, uy, uz = dx / dist, dy / dist, dz / dist
            disp[a][0] -= ux * f; disp[a][1] -= uy * f; disp[a][2] -= uz * f
            disp[b][0] += ux * f; disp[b][1] += uy * f; disp[b][2] += uz * f
        t = 0.10 * (1 - it / 420)
        for i in range(n):
            dl = math.sqrt(sum(c * c for c in disp[i])) or 0.01
            for c in range(3):
                pos[i][c] += disp[i][c] / dl * min(dl, t)
    # zentrieren + skalieren
    for c in range(3):
        m = sum(p[c] for p in pos) / n
        for p in pos: p[c] -= m
    span = max(math.sqrt(sum(c * c for c in p)) for p in pos) or 1
    cx, cy, R = W / 2, H / 2 + 18, 165
    ay, ax = 0.6, 0.35
    P = [project(p[0] / span, p[1] / span, p[2] / span, ay, ax, R, cx, cy) for p in pos]
    out = []
    for a, b in EDGES:
        pa, pb = P[a], P[b]; d = ((pa[2] + pb[2]) / 2 + 1) / 2
        out.append(f"<line x1='{pa[0]:.1f}' y1='{pa[1]:.1f}' x2='{pb[0]:.1f}' y2='{pb[1]:.1f}' "
                   f"stroke='#7896d7' stroke-opacity='{0.10 + d * 0.38:.2f}'/>")
    for i in sorted(range(n), key=lambda j: P[j][2]):
        p = P[i]; d = (p[2] + 1) / 2; rad = 3 + d * 4.5
        out.append(node_circle(p[0], p[1], NODES[i]["t"], d, rad))
        if NODES[i]["t"] in ("topic", "target", "policy", "strategy"):
            out.append(label(p[0], p[1], NODES[i]["l"], d, rad))
    return frame("".join(out), "B · Kraft-Cluster (organisch)")

# ----------------------------------------------------------------- C) Chord-Ring
def layout_chord():
    cx, cy, R = W / 2, H / 2 + 20, 165
    order = ["topic", "iro", "target", "kpi", "initiative", "policy", "strategy"]
    grouped = sorted(range(len(NODES)), key=lambda i: (order.index(NODES[i]["t"]) if NODES[i]["t"] in order else 9, NODES[i]["l"]))
    n = len(grouped); ang = {}
    gap = 0.16
    # Sektorlücken zwischen Typgruppen
    seq = []; prev = None; pad = 0.0
    for i in grouped:
        if prev is not None and NODES[i]["t"] != NODES[prev]["t"]:
            pad += gap
        seq.append((i, pad)); prev = i
    total = 2 * math.pi
    span = total - pad
    step = span / max(1, n)
    acc = 0.0; prevpad = 0.0
    for k, (i, pd) in enumerate(seq):
        a = (pd) + k * step
        ang[i] = a
    sq = 0.55  # vertikale Stauchung -> 3D-Ring-Anmutung
    pos = {i: (cx + math.cos(ang[i]) * R, cy + math.sin(ang[i]) * R * sq) for i in range(len(NODES))}
    out = [f"<ellipse cx='{cx}' cy='{cy}' rx='{R}' ry='{R*sq:.0f}' fill='none' stroke='#30363d' stroke-opacity='0.5'/>"]
    for a, b in EDGES:
        xa, ya = pos[a]; xb, yb = pos[b]
        out.append(f"<path d='M{xa:.1f},{ya:.1f} Q{cx:.1f},{cy:.1f} {xb:.1f},{yb:.1f}' "
                   f"fill='none' stroke='#7896d7' stroke-opacity='0.30'/>")
    for i in range(len(NODES)):
        xa, ya = pos[i]
        out.append(node_circle(xa, ya, NODES[i]["t"], 0.7, 4.5))
        if NODES[i]["t"] in ("topic", "target", "policy", "strategy"):
            anchor = "start" if math.cos(ang[i]) >= 0 else "end"
            dx = 7 if anchor == "start" else -7
            out.append(f"<text x='{xa+dx:.1f}' y='{ya+3:.1f}' fill='#e3e8ee' fill-opacity='0.7' "
                       f"font-size='9.5' text-anchor='{anchor}'>{html.escape(NODES[i]['l'])}</text>")
    return frame("".join(out), "C · Chord-Ring (ein Kreis)")

# ----------------------------------------------- D) Fluss-Diagramm (Sankey-Stil)
def layout_flow():
    FW, FH = 860, 560
    STAGE = {"iro": 0, "policy": 1, "strategy": 1, "target": 1, "kpi": 2, "initiative": 2}
    cols = {0: [], 1: [], 2: []}
    for i, n in enumerate(NODES):
        s = STAGE.get(n["t"])
        if s is not None:
            cols[s].append(i)
    # nur Kanten zwischen benachbarten Spalten
    adj = {i: [] for i in range(len(NODES))}
    fedges = []
    for a, b in EDGES:
        sa, sb = STAGE.get(NODES[a]["t"]), STAGE.get(NODES[b]["t"])
        if sa is None or sb is None or abs(sa - sb) != 1:
            continue
        lo, hi = (a, b) if sa < sb else (b, a)
        fedges.append((lo, hi)); adj[lo].append(hi); adj[hi].append(lo)
    X = {0: 120, 1: 430, 2: 740}
    BW = 168
    yof = {}
    def assign_y(col):
        n = len(col)
        if not n: return
        avail = FH - 110; top = 90; sp = avail / n
        for k, i in enumerate(col):
            yof[i] = top + (k + 0.5) * sp
    def order_by(col, ref):
        def key(i):
            ys = [yof[j] for j in adj[i] if j in ref]
            return sum(ys) / len(ys) if ys else 1e9
        col.sort(key=key)
    cols[0].sort(key=lambda i: NODES[i]["l"]); assign_y(cols[0])
    order_by(cols[1], set(cols[0])); assign_y(cols[1])
    order_by(cols[2], set(cols[1])); assign_y(cols[2])
    order_by(cols[1], set(cols[0]) | set(cols[2])); assign_y(cols[1])  # Rück-Sweep
    out = [f"<rect width='{FW}' height='{FH}' fill='{BG}' rx='10'/>",
           f"<text x='20' y='30' fill='#e3e8ee' font-size='15' font-weight='600'>D · Fluss-Diagramm (Sankey-Stil)</text>",
           f"<text x='20' y='49' fill='#8a97a6' font-size='11'>{html.escape(TITLE)} — Auswirkung/Risiko → Steuerung → Messung &amp; Maßnahme</text>"]
    heads = [("Auswirkungen · Risiken · Chancen", 0), ("Steuerung — Policy · Ziel · Strategie", 1), ("Messung & Maßnahmen", 2)]
    for txt, s in heads:
        out.append(f"<text x='{X[s]}' y='76' fill='#8a97a6' font-size='10.5' font-weight='600' text-anchor='middle'>{html.escape(txt)}</text>")
    # Bänder
    for lo, hi in fedges:
        x1 = X[STAGE[NODES[lo]["t"]]] + BW / 2; x2 = X[STAGE[NODES[hi]["t"]]] - BW / 2
        y1, y2 = yof[lo], yof[hi]; mx = (x1 + x2) / 2
        c = COL.get(NODES[lo]["t"], "#8a97a6")
        out.append(f"<path d='M{x1:.1f},{y1:.1f} C{mx:.1f},{y1:.1f} {mx:.1f},{y2:.1f} {x2:.1f},{y2:.1f}' "
                   f"fill='none' stroke='{c}' stroke-opacity='0.32' stroke-width='1.6'/>")
    # Knoten als beschriftete Kästen
    for i in range(len(NODES)):
        if STAGE.get(NODES[i]["t"]) is None: continue
        s = STAGE[NODES[i]["t"]]; x = X[s] - BW / 2; y = yof[i] - 11; c = COL.get(NODES[i]["t"], "#8a97a6")
        gap = (NODES[i]["t"] == "iro" and not adj[i])  # ungesteuerte IRO
        stroke = "#f85149" if gap else c
        sw = "1.8" if gap else "1"
        out.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{BW}' height='22' rx='5' "
                   f"fill='{c}' fill-opacity='0.16' stroke='{stroke}' stroke-opacity='0.9' stroke-width='{sw}'/>")
        lab = NODES[i]["l"]
        out.append(f"<text x='{x+9:.1f}' y='{yof[i]+3.5:.1f}' fill='#e3e8ee' font-size='10'>{html.escape(lab)}</text>")
        if gap:
            out.append(f"<text x='{x+BW-7:.1f}' y='{yof[i]+3.5:.1f}' fill='#f85149' font-size='10' text-anchor='end'>● Lücke</text>")
    return (f"<svg viewBox='0 0 {FW} {FH}' xmlns='http://www.w3.org/2000/svg' "
            f"font-family='-apple-system,Segoe UI,sans-serif'>{''.join(out)}</svg>")

OUTDIR = ROOT / "cockpit" / "_layout-previews"
OUTDIR.mkdir(parents=True, exist_ok=True)
for name, fn in [("A-orbits", layout_orbits), ("B-force", layout_force),
                 ("C-chord", layout_chord), ("D-flow", layout_flow)]:
    (OUTDIR / f"layout-{name}.svg").write_text(fn(), encoding="utf-8")
    print("geschrieben:", (OUTDIR / f"layout-{name}.svg").name)
