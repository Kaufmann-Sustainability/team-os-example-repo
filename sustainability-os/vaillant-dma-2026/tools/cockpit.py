#!/usr/bin/env python3
"""
Cockpit-Generator — self-rendered, verlinktes HTML aus dem Objektgraphen.

Erzeugt eine navigierbare Mini-Site unter cockpit/:
  - JEDES Objekt = eine Seite (Metadaten, Text, aus-/eingehende Kanten als Links)
  - THEMEN bekommen zusätzlich die KURATIERTE Cockpit-Ansicht
    (IRO-Abdeckung · Ziele mit Reifegrad · KPIs mit Ist-Werten · Maßnahmen · Policies · Lücken)
  - index.html listet die Themen als Einstieg

Navigation = den getypten Kanten folgen (klicken). Kein Server, reine Dateien, in Git.
Aufruf:  python3 tools/cockpit.py      Benötigt: PyYAML.
"""
from __future__ import annotations
import html, re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cockpit"
FM = re.compile(r"^---\n(.*?)\n---(.*)$", re.DOTALL)
H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)

# Metadaten-Felder, die KEINE Objekt-Kante sind (nur anzeigen, nicht verlinken).
META = {"id", "type", "owner", "status", "stand", "vertraulichkeit", "review_zyklus",
        "esrs_bezug", "quelle", "offene_punkte", "einheit", "datum", "begriff",
        "baseline_wert", "baseline_jahr", "zielwert", "zieljahr", "geltungsbereich",
        "betrag", "waehrung", "jahr", "wert", "confidence", "genehmiger", "gremium",
        "wahrscheinlichkeit", "auswirkung", "iro_typ", "wesentlich", "stakeholder_typ",
        "concept", "esrs_datapoint", "framework", "datentyp", "katalog_version",
        "katalog_dp", "berichtsjahr", "version", "system", "aktualisierung",
        "verlaesslichkeit", "land", "name", "rolle", "gegenmassnahme"}

# Status -> Farbklasse
def badge(status):
    s = (status or "").lower()
    if s in ("aktiv", "final", "erteilt", "in-umsetzung", "abgeschlossen", "wesentlich"):
        return "ok"
    if s in ("offen", "geplant", "entwurf", "in-arbeit"):
        return "warn"
    return "neutral"


def load():
    objs = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        fm = yaml.safe_load(m.group(1)) or {}
        t = H1.search(m.group(2))
        oid = fm.get("id", p.stem)
        objs[oid] = {"fm": fm, "body": m.group(2).strip(),
                     "title": (t.group(1).strip() if t else oid)}
    return objs


def edges_out(fm):
    """(feld, [ids]) für alle Felder, die auf Objekte zeigen (nicht Metadaten)."""
    out = []
    for k, v in fm.items():
        if k in META or k == "type":
            continue
        ids = [v] if isinstance(v, str) else (v if isinstance(v, list) else [])
        ids = [i for i in ids if isinstance(i, str)]
        if ids:
            out.append((k, ids))
    return out


def md(text):
    """Sehr leichtes Markdown -> HTML (Überschriften, Zitat, fett, code, Absätze)."""
    out, para = [], []
    def flush():
        if para:
            out.append("<p>" + " ".join(para) + "</p>"); para.clear()
    for ln in text.splitlines():
        s = ln.rstrip()
        if not s:
            flush(); continue
        e = html.escape(s)
        e = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e)
        e = re.sub(r"`(.+?)`", r"<code>\1</code>", e)
        if s.startswith("# "):
            flush(); out.append(f"<h2>{e[6:]}</h2>")
        elif s.startswith("> "):
            flush(); out.append(f"<blockquote>{e[6:]}</blockquote>")
        elif s.startswith("- "):
            out.append(f"<div class='li'>• {e[6:]}</div>")
        else:
            para.append(e)
    flush()
    return "\n".join(out)


CSS = """
:root{--bg:#0f1419;--card:#1a2029;--line:#2a323d;--txt:#e3e8ee;--mut:#8a97a6;
--ok:#3fb950;--warn:#d29922;--neutral:#6e7681;--link:#58a6ff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);
font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--link);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1000px;margin:0 auto;padding:24px}
.crumb{color:var(--mut);font-size:13px;margin-bottom:16px}
h1{font-size:24px;margin:0 0 4px}.sub{color:var(--mut);margin-bottom:20px}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:12px;font-weight:600}
.badge.ok{background:rgba(63,185,80,.15);color:var(--ok)}
.badge.warn{background:rgba(210,153,34,.15);color:var(--warn)}
.badge.neutral{background:rgba(110,118,129,.15);color:var(--neutral)}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:14px 0}
.card h3{margin:0 0 10px;font-size:15px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}
table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);font-size:14px;vertical-align:top}
th{color:var(--mut);font-weight:600}
code{background:#0d1117;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:12.5px}
.bar{display:inline-block;width:90px;height:8px;background:#0d1117;border-radius:4px;overflow:hidden;vertical-align:middle}
.bar>i{display:block;height:100%;background:var(--ok)}
.bar.low>i{background:var(--warn)}
blockquote{border-left:3px solid var(--line);margin:6px 0;padding:2px 12px;color:var(--mut)}
.li{margin:2px 0}.gap{color:var(--warn)}.meta td:first-child{color:var(--mut);width:160px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:700px){.grid{grid-template-columns:1fr}}
"""


def main():
    objs = load()
    OUT.mkdir(exist_ok=True)
    # Reverse-Index: eingehende Kanten
    incoming = {oid: [] for oid in objs}
    for oid, o in objs.items():
        for feld, ids in edges_out(o["fm"]):
            for tid in ids:
                if tid in incoming:
                    incoming[tid].append((oid, feld))

    def link(i):
        if i in objs:
            return f"<a href='{i}.html'><code>{html.escape(i)}</code></a>"
        return f"<code>{html.escape(i)}</code>"

    def rev(tid, edge, typ=None):
        return [s for s, f in incoming.get(tid, []) if f == edge and (typ is None or objs[s]['fm'].get('type') == typ)]

    def target_maturity(tid):
        fm = objs[tid]["fm"]
        checks = {
            "Owner": bool(fm.get("owner")) and fm.get("owner") != "person-unassigned",
            "Messbar": all(fm.get(k) is not None for k in ("baseline_wert", "zielwert", "zieljahr", "einheit", "geltungsbereich")),
            "≥1 IRO": bool(fm.get("addresses")),
            "≥1 KPI": bool(fm.get("measured_by")),
            "≥1 Maßnahme": bool(fm.get("supported_by")),
            "Annahme": bool(rev(tid, "underpins")),
            "Freigabe": bool(rev(tid, "approves")),
            "Risiko": bool(rev(tid, "threatens")),
        }
        return sum(checks.values()), len(checks), checks

    def page(title, sub, body, crumb="<a href='index.html'>← Cockpits</a>"):
        return (f"<!doctype html><meta charset=utf-8><title>{html.escape(title)}</title>"
                f"<style>{CSS}</style><div class=wrap><div class=crumb>{crumb}</div>"
                f"<h1>{html.escape(title)}</h1><div class=sub>{sub}</div>{body}</div>")

    # --- generische Objekt-Seite ---
    for oid, o in objs.items():
        fm = o["fm"]
        meta = "".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(str(fm.get(k)))}</td></tr>"
                       for k in ("type", "owner", "status", "stand", "vertraulichkeit", "esrs_bezug")
                       if fm.get(k) is not None)
        out_html = ""
        for feld, ids in edges_out(fm):
            out_html += f"<tr><td>{html.escape(feld)}</td><td>{' '.join(link(i) for i in ids)}</td></tr>"
        in_html = "".join(f"<tr><td>{link(s)}</td><td>{html.escape(f)}</td></tr>" for s, f in incoming.get(oid, []))
        sub = f"<span class='badge {badge(fm.get('status'))}'>{html.escape(str(fm.get('status','')))}</span> &nbsp;<code>{html.escape(oid)}</code> · {html.escape(str(fm.get('type','')))}"
        cards = f"<div class=card><h3>Metadaten</h3><table class=meta>{meta}</table></div>"
        if out_html:
            cards += f"<div class=card><h3>Beziehungen → </h3><table>{out_html}</table></div>"
        if in_html:
            cards += f"<div class=card><h3>← referenziert von</h3><table>{in_html}</table></div>"
        if o["body"]:
            cards += f"<div class=card><h3>Beschreibung</h3>{md(o['body'])}</div>"
        crumb = "<a href='index.html'>← Cockpits</a>"
        # Themen: kuratierte Cockpit-Ansicht voranstellen
        if fm.get("type") == "topic":
            cards = topic_cockpit(oid, objs, link, rev, target_maturity) + cards
        (OUT / f"{oid}.html").write_text(page(o["title"], sub, cards, crumb), encoding="utf-8")

    # --- index ---
    topics = sorted([oid for oid, o in objs.items() if o["fm"].get("type") == "topic"])
    rows = ""
    for tid in topics:
        fm = objs[tid]["fm"]
        n_iro = len(fm.get("has_iro") or []); n_t = len(fm.get("has_target") or [])
        rows += (f"<tr><td><a href='{tid}.html'>{html.escape(objs[tid]['title'])}</a></td>"
                 f"<td><span class='badge {badge(fm.get('status'))}'>{html.escape(str(fm.get('status','')))}</span></td>"
                 f"<td>{html.escape(str(fm.get('esrs_bezug','')))}</td><td>{n_iro} IROs · {n_t} Ziele</td></tr>")
    body = (f"<div class=card><h3>Themen</h3><table><tr><th>Thema</th><th>Status</th>"
            f"<th>Standard</th><th>Umfang</th></tr>{rows}</table></div>"
            f"<div class=sub>{len(objs)} Objekte gesamt · jedes ist eine Seite, jede Kante ein Link.</div>")
    (OUT / "index.html").write_text(page("Sustainability OS — Cockpits", "Navigierbarer Objektgraph", body, "Start"), encoding="utf-8")
    print(f"✓ {len(objs)+1} Seiten -> {OUT}/index.html  ({len(topics)} Themen-Cockpits)")


def topic_cockpit(tid, objs, link, rev, target_maturity):
    fm = objs[tid]["fm"]
    def title(i): return html.escape(objs[i]["title"]) if i in objs else i

    # IRO-Abdeckung: wesentliche IRO adressiert von Policy/Target/Strategy?
    iros = fm.get("has_iro") or []
    addressers = {}  # iro -> [quelle]
    for oid, o in objs.items():
        for tgt in (o["fm"].get("addresses") or []):
            if tgt in iros:
                addressers.setdefault(tgt, []).append(oid)
    iro_rows = ""
    for i in iros:
        wes = str(objs[i]["fm"].get("wesentlich", "")).lower() in ("ja", "true")
        if not wes:
            continue
        adr = addressers.get(i, [])
        mark = ("<span class='badge ok'>adressiert</span>" if adr else "<span class='badge warn'>OFFEN</span>")
        iro_rows += f"<tr><td>{link(i)}</td><td>{mark}</td><td>{' '.join(link(a) for a in adr) or '<span class=gap>—</span>'}</td></tr>"
    n_open = sum(1 for i in iros if str(objs[i]['fm'].get('wesentlich','')).lower() in ('ja','true') and not addressers.get(i))
    cov = (f"<div class=card><h3>IRO-Abdeckung — {'⚠ '+str(n_open)+' offen' if n_open else '✅ vollständig'}</h3>"
           f"<table><tr><th>wesentliche IRO</th><th>Status</th><th>adressiert durch</th></tr>{iro_rows}</table></div>")

    # Ziele mit Reifegrad + RASCI + Performance
    trow = ""
    for t in fm.get("has_target") or []:
        tf = objs[t]["fm"]; n, tot, _ = target_maturity(t)
        pct = round(100*n/tot); low = " low" if pct < 75 else ""
        acc = link(tf.get("owner")) if tf.get("owner") else "—"
        resp = " ".join(link(r) for r in (tf.get("responsible") or [])) or "<span class=gap>—</span>"
        # letzter KPI-Wert
        val = ""
        for k in (tf.get("measured_by") or []):
            vals = sorted([(objs[v]['fm'].get('jahr'), objs[v]['fm'].get('wert')) for v in rev(k, "for_kpi", "kpi-value") if objs[v]['fm'].get('jahr')], key=lambda x: x[0])
            if vals: val = f"{vals[-1][1]} ({vals[-1][0]})"
        trow += (f"<tr><td><a href='{t}.html'>{title(t)}</a></td>"
                 f"<td><span class='bar{low}'><i style='width:{pct}%'></i></span> {pct}%</td>"
                 f"<td>{html.escape(str(tf.get('zielwert')))} {html.escape(str(tf.get('einheit','')))[:14]}</td>"
                 f"<td>{val or '<span class=gap>kein Ist</span>'}</td>"
                 f"<td>A:{acc}<br>R:{resp}</td></tr>")
    targets = (f"<div class=card><h3>Ziele — Reifegrad · RASCI · Ist-Wert</h3>"
               f"<table><tr><th>Ziel</th><th>Reifegrad</th><th>Zielwert</th><th>Ist</th><th>Verantwortung</th></tr>{trow}</table></div>")

    # Maßnahmen + Policies (kompakt)
    inis = " ".join(f"<a href='{i}.html'>{title(i)}</a>" for i in (fm.get("has_initiative") or []))
    pols = [oid for oid, o in objs.items() if o["fm"].get("type") == "policy" and tid in (o["fm"].get("concerns") or [])]
    polh = " ".join(f"<a href='{p}.html'>{title(p)}</a>" for p in pols) or "<span class=gap>—</span>"
    extra = (f"<div class=grid><div class=card><h3>Maßnahmen ({len(fm.get('has_initiative') or [])})</h3>{inis or '—'}</div>"
             f"<div class=card><h3>Policies ({len(pols)})</h3>{polh}</div></div>")
    return cov + targets + extra


if __name__ == "__main__":
    main()
