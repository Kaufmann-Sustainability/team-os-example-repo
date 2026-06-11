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
    if s in ("aktiv", "final", "erteilt", "in-umsetzung", "abgeschlossen", "wesentlich",
             "in-kraft", "verabschiedet", "freigegeben"):
        return "ok"
    if s in ("offen", "geplant", "entwurf", "in-arbeit", "in-planung"):
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
.badge.bad{background:rgba(248,81,73,.15);color:#f85149}
.tiles{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:14px 0}
@media(max-width:700px){.tiles{grid-template-columns:repeat(2,1fr)}}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.tile .n{font-size:26px;font-weight:700;line-height:1.1}.tile .l{color:var(--mut);font-size:12px;margin-top:4px}
.tile.ok .n{color:var(--ok)}.tile.warn .n{color:var(--warn)}.tile.bad .n{color:#f85149}
.prog{display:inline-block;width:120px;height:9px;background:#0d1117;border-radius:5px;overflow:hidden;vertical-align:middle;position:relative}
.prog>i{display:block;height:100%;background:var(--link)}
.miss{color:#f85149;font-size:12px}.dim{color:var(--mut);font-size:12px}
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
.attn{border:1px solid var(--line);border-left:4px solid var(--neutral);border-radius:10px;background:var(--card);padding:16px 18px;margin:16px 0}
.attn.bad{border-left-color:#f85149}.attn.warn{border-left-color:var(--warn)}.attn.ok{border-left-color:var(--ok)}
.attn-h{font-weight:700;font-size:16px;margin-bottom:8px}
.attn.bad .attn-h{color:#f85149}.attn.warn .attn-h{color:var(--warn)}.attn.ok .attn-h{color:var(--ok)}
.attn ul{margin:0;padding-left:20px}.attn li{margin:5px 0}
.attn li.bad::marker{color:#f85149}.attn li.warn::marker{color:var(--warn)}
.hint{color:var(--mut);font-size:12.5px;font-weight:400;text-transform:none;letter-spacing:0;margin:-4px 0 12px}
tbody tr:nth-child(even){background:rgba(255,255,255,.02)}
td,th{padding:8px 10px}
.prog>i{background:#6e7bd2}.prog.pg>i{background:var(--ok)}.prog.pgbad>i{background:#f85149}
.unit{color:var(--mut);font-size:11px}.tile{cursor:default}
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
        # Themen zeigen ihre Beziehungen in den kuratierten Cockpit-Tabellen (Klartext),
        # daher die generischen ID-Tabellen dort weglassen.
        if out_html and fm.get("type") != "topic":
            cards += f"<div class=card><h3>Beziehungen → </h3><table>{out_html}</table></div>"
        if in_html and fm.get("type") != "topic":
            cards += f"<div class=card><h3>← referenziert von</h3><table>{in_html}</table></div>"
        if o["body"]:
            cards += f"<div class=card><h3>Beschreibung</h3>{md(o['body'])}</div>"
        crumb = "<a href='index.html'>← Cockpits</a>"
        # Themen: Kontext-Subheader + kuratierte Cockpit-Ansicht voranstellen
        if fm.get("type") == "topic":
            owner_r = objs.get(fm.get("owner"), {}).get("fm", {}).get("rolle") or str(fm.get("owner", "—"))
            ti = fm.get("has_iro") or []
            n_wes = sum(1 for i in ti if str(objs.get(i, {}).get("fm", {}).get("wesentlich", "")).lower() in ("ja", "true"))
            sub = (f"<span class='badge {badge(fm.get('status'))}'>{html.escape(str(fm.get('status','')))}</span> &nbsp;"
                   f"ESRS {html.escape(str(fm.get('esrs_bezug','')))} · verantwortet von {html.escape(owner_r)} · "
                   f"Review {html.escape(str(fm.get('review_zyklus','—')))} · Stand {html.escape(str(fm.get('stand','—')))} · "
                   f"{n_wes}/{len(ti)} IROs wesentlich")
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


def _num(x):
    try:
        return float(str(x).replace(",", ".").split()[0])
    except Exception:
        return None


def topic_cockpit(tid, objs, link, rev, target_maturity):
    fm = objs[tid]["fm"]
    def title(i): return html.escape(objs[i]["title"]) if i in objs else i

    def dname(i, n=54):  # Anzeigename: redundantes Typ-Präfix weg, gekürzt
        t = objs[i]["title"] if i in objs else str(i)
        t = re.sub(r"^(Ziel|Maßnahme|Policy|Strategie|KPI|IRO[^:]*):\s*", "", t)
        return html.escape(t if len(t) <= n else t[:n - 1].rstrip() + "…")

    def who(i):  # Person -> Rolle (menschenlesbar), sonst Titel
        f = objs.get(i, {}).get("fm", {})
        return html.escape(f.get("rolle") or (objs[i]["title"] if i in objs else str(i)))

    def who_link(i):
        return f"<a href='{i}.html'>{who(i)}</a>" if i in objs else who(i)

    def name_link(i):  # Objekt -> Titel-Link (statt ID-Code)
        return f"<a href='{i}.html'>{dname(i)}</a>" if i in objs else html.escape(str(i))

    def short(t, n=110):
        t = (t or "").strip()
        return html.escape(t if len(t) <= n else t[:n - 1].rstrip() + "…")

    def money(i):  # Initiative -> erstes Budget formatiert
        for b in (objs.get(i, {}).get("fm", {}).get("has_budget") or []):
            v = _num(objs.get(b, {}).get("fm", {}).get("betrag")); w = objs[b]["fm"].get("waehrung", "")
            if v is None:
                return ""
            unit = (f"{v/1e9:.1f} Mrd" if v >= 1e9 else f"{v/1e6:.0f} Mio" if v >= 1e6 else f"{v/1e3:.0f}k" if v >= 1e3 else f"{v:.0f}")
            return f"<a href='{b}.html'>{unit} {html.escape(w)}</a>"
        return "<span class=dim>—</span>"

    def iro_desc(i):
        m = re.search(r"##\s*Beschreibung\s*\n+(.+)", objs.get(i, {}).get("body", ""))
        return m.group(1).strip() if m else ""

    def typ_badge(i):
        t = str(objs.get(i, {}).get("fm", {}).get("iro_typ", "")) or "IRO"
        cl = "ok" if ("positiv" in t.lower() or "chance" in t.lower() or "opportun" in t.lower()) else \
             "bad" if "negativ" in t.lower() else "warn" if ("risk" in t.lower() or "risiko" in t.lower()) else "neutral"
        return f"<span class='badge {cl}'>{html.escape(t)}</span>"

    def kpi_latest(k):
        vals = sorted([(_num(objs[v]['fm'].get('jahr')), objs[v]['fm'].get('wert'))
                       for v in rev(k, "for_kpi", "kpi-value") if objs[v]['fm'].get('jahr') is not None],
                      key=lambda x: x[0] or 0)
        return vals[-1] if vals else None  # (jahr, wert)

    def kpi_trend(k):
        for tobj in rev(k, "for_kpi", "trend"):
            return objs[tobj]['fm'].get('bewertung')
        return None

    def kpi_forecast(k):
        fcs = [(objs[v]['fm'].get('jahr'), objs[v]['fm'].get('wert')) for v in rev(k, "for_kpi", "forecast")]
        return fcs[-1] if fcs else None

    def trend_badge(b):
        if b == "on-track":
            return "<span class='badge ok'>auf Kurs</span>"
        if b == "off-track":
            return "<span class='badge bad'>nicht auf Kurs</span>"
        return "<span class='dim'>kein Trend</span>"

    # IRO-Abdeckung: wesentliche IRO adressiert von Policy/Target/Strategy?
    iros = fm.get("has_iro") or []
    addressers = {}  # iro -> [quelle]
    for oid, o in objs.items():
        for tgt in (o["fm"].get("addresses") or []):
            if tgt in iros:
                addressers.setdefault(tgt, []).append(oid)
    iro_rows = ""
    for i in iros:
        if str(objs[i]["fm"].get("wesentlich", "")).lower() not in ("ja", "true"):
            continue
        adr = addressers.get(i, [])
        mark = ("<span class='badge ok'>adressiert</span>" if adr else "<span class='badge warn'>OFFEN</span>")
        nr = html.escape(str(objs[i]["fm"].get("iro_nr", i)))
        adr_h = "<br>".join(name_link(a) for a in adr) or "<span class=gap>noch nicht gesteuert</span>"
        iro_rows += (f"<tr><td><a href='{i}.html'>{nr}</a><br><span class=dim>{short(iro_desc(i),140)}</span></td>"
                     f"<td>{typ_badge(i)}</td><td>{mark}</td><td>{adr_h}</td></tr>")
    n_open = sum(1 for i in iros if str(objs[i]['fm'].get('wesentlich','')).lower() in ('ja','true') and not addressers.get(i))
    cov = (f"<div class=card><h3>IRO-Abdeckung — {'⚠ '+str(n_open)+' offen' if n_open else '✅ vollständig'}</h3>"
           f"<div class=hint>Jede wesentliche Auswirkung, jedes Risiko und jede Chance (IRO aus der Wesentlichkeits&shy;analyse) "
           f"muss durch Strategie, Policy oder Ziel gesteuert sein — ESRS-Pflicht.</div>"
           f"<table><tr><th>Wesentliche Auswirkung / Risiko / Chance</th><th>Typ</th><th>Status</th>"
           f"<th>gesteuert durch</th></tr>{iro_rows}</table></div>")

    # ---- Formatierungs-Helfer ----
    def fmt(x): return html.escape(str(x))
    def yr(x):
        try: return str(int(x))
        except Exception: return ""
    def fmtnum(v):
        try: v = float(v)
        except Exception: return ""
        return str(int(v)) if v.is_integer() else f"{v:.1f}"
    def einh(f):
        u = str(f.get("einheit", "")).strip()
        if "%" in u:
            return "%"
        u = u.split("/")[0].strip()
        return html.escape(u if len(u) <= 10 else u.split()[0])
    def typ_word(i):
        t = str(objs.get(i, {}).get("fm", {}).get("iro_typ", "")).lower()
        return "Chance" if ("positiv" in t or "chance" in t or "opportun" in t) else \
               "Risiko" if ("risk" in t or "risiko" in t) else "Auswirkung"

    # ---- Ziele: Status (Prognose ggü. Ziel) · Fortschritt · Steuerung · Verantwortung ----
    targets_ids = fm.get("has_target") or []
    mats, on_track, off_track = [], 0, 0
    off_targets, miss_freigabe, miss_risiko = [], [], []
    trow = ""
    for t in targets_ids:
        tf = objs[t]["fm"]; n, tot, checks = target_maturity(t); pct = round(100 * n / tot); mats.append(pct)
        miss = [k for k, ok in checks.items() if not ok]
        if not checks["Freigabe"]: miss_freigabe.append(t)
        if not checks["Risiko"]: miss_risiko.append(t)
        b, z = _num(tf.get("baseline_wert")), _num(tf.get("zielwert"))
        ist = trend = fc = None
        for k in (tf.get("measured_by") or []):
            lv = kpi_latest(k)
            if lv and ist is None: ist = lv
            trend = trend or kpi_trend(k); fc = fc or kpi_forecast(k)
        if trend == "on-track": on_track += 1
        elif trend == "off-track": off_track += 1
        # Lücke: Prognose ggü. Ziel
        gap_txt, gap_bad = "", False
        fv = _num(fc[1]) if fc else None
        if fv is not None and z is not None and b is not None and b != z:
            if z < b and fv - z > 0: gap_txt, gap_bad = f"+{fmtnum(fv - z)} {einh(tf)} über Ziel", True
            elif z > b and z - fv > 0: gap_txt, gap_bad = f"−{fmtnum(z - fv)} {einh(tf)} unter Ziel", True
            else: gap_txt = "Ziel erreichbar"
        # Status-Urteil
        if trend == "off-track": sv = ("bad", "Gefährdet"); off_targets.append((t, gap_txt, fc, z, tf))
        elif trend == "on-track": sv = ("ok", "Auf Kurs")
        elif ist is not None: sv = ("neutral", "In Umsetzung")
        else: sv = ("neutral", "Kein Tracking")
        status_cell = f"<span class='badge {sv[0]}'>{sv[1]}</span>"
        if fc:
            gap_red = gap_bad and trend != "on-track"
            g = (f" · <span class=miss>{gap_txt}</span>" if gap_red else (f" · {gap_txt}" if gap_txt else ""))
            status_cell += f"<div class=dim>Prognose {fmt(fc[1])} ({yr(fc[0])}){g}</div>"
        # Fortschrittsbalken (grün; rot bei off-track)
        if b is not None and z is not None and ist is not None and _num(ist[1]) is not None and b != z:
            p = max(0, min(100, round(100 * (_num(ist[1]) - b) / (z - b))))
            pg = "pgbad" if trend == "off-track" else "pg"
            prog_html = (f"<span class='prog {pg}'><i style='width:{p}%'></i></span> {p}%"
                         f"<div class=dim>{fmt(tf.get('baseline_wert'))} → <b>{fmt(ist[1])}</b> ({yr(ist[0])}) → {fmt(tf.get('zielwert'))} <span class=unit>{einh(tf)}</span></div>")
        else:
            prog_html = "<span class=dim>noch kein Ist-Wert</span>"
        # Steuerung = Vollständigkeit (indigo)
        reif = (f"<span class='prog'><i style='width:{pct}%'></i></span> {pct}%"
                + (f"<div class=miss>offen: {', '.join(miss)}</div>" if miss else ""))
        resp = (tf.get("responsible") or [])
        verant = (who_link(tf.get("owner")) if tf.get("owner") else "—") + \
                 (f"<div class=dim>+ {', '.join(who(r) for r in resp)}</div>" if resp else "")
        trow += (f"<tr><td><a href='{t}.html'>{dname(t)}</a></td><td>{status_cell}</td>"
                 f"<td>{prog_html}</td><td>{reif}</td><td>{verant}</td></tr>")
    targets = (f"<div class=card><h3>Ziele</h3>"
               f"<div class=hint><b>Status</b> = Prognose ggü. Ziel · <b>Fortschritt</b> = Baseline→Ist→Ziel · "
               f"<b>Steuerung</b> = Vollständigkeit des Apparats (8 Pflichten je Ziel)</div>"
               f"<table><tr><th>Ziel</th><th>Status</th><th>Fortschritt</th><th>Steuerung</th><th>Verantwortung</th></tr>{trow}</table></div>")

    # KPI-Sektion: Ist · Trend · Prognose
    krow = ""
    for k in fm.get("has_kpi") or []:
        kf = objs[k]["fm"]; u = html.escape(str(kf.get("einheit", "")).split("/")[0].strip()[:12])
        lv = kpi_latest(k); fc = kpi_forecast(k); tr = kpi_trend(k)
        ist = (f"<b>{html.escape(str(lv[1]))}</b> <span class=unit>{u}</span> <span class=dim>({int(lv[0]) if lv[0] else ''})</span>"
               if lv else "<span class=gap>kein Ist-Wert</span>")
        prg = f"{html.escape(str(fc[1]))} <span class=dim>({fc[0]})</span>" if fc else "<span class=dim>—</span>"
        krow += (f"<tr><td><a href='{k}.html'>{dname(k)}</a></td><td>{ist}</td>"
                 f"<td>{trend_badge(tr)}</td><td>{prg}</td></tr>")
    kpis = (f"<div class=card><h3>KPIs</h3><div class=hint>Aktueller Ist-Wert, Trend und Prognose je Kennzahl</div>"
            f"<table><tr><th>KPI</th><th>Ist-Wert</th><th>Trend</th><th>Prognose</th></tr>{krow}</table></div>")

    # Maßnahmen — Owner · Status · Budget
    inis = fm.get("has_initiative") or []
    def stat(i): f = objs.get(i, {}).get("fm", {}); return f"<span class='badge {badge(f.get('status'))}'>{html.escape(str(f.get('status','')))}</span>"
    irow = "".join(f"<tr><td><a href='{i}.html'>{dname(i)}</a></td><td>{who_link(objs[i]['fm'].get('owner'))}</td>"
                   f"<td>{stat(i)}</td><td>{money(i)}</td></tr>" for i in inis)
    mass = (f"<div class=card><h3>Maßnahmen ({len(inis)})</h3>"
            f"<table><tr><th>Maßnahme</th><th>Owner</th><th>Status</th><th>Budget</th></tr>{irow}</table></div>"
            if inis else "<div class=card><h3>Maßnahmen (0)</h3><span class=gap>—</span></div>")

    # Policies — Owner · Geltungsbereich · Status · letztes Update
    pols = [o for o, x in objs.items() if x["fm"].get("type") == "policy" and tid in (x["fm"].get("concerns") or [])]
    prow = "".join(f"<tr><td><a href='{p}.html'>{dname(p)}</a></td><td>{who_link(objs[p]['fm'].get('owner'))}</td>"
                   f"<td>{short(objs[p]['fm'].get('geltungsbereich',''),60)}</td><td>{stat(p)}</td>"
                   f"<td class=dim>{html.escape(str(objs[p]['fm'].get('stand','—')))}</td></tr>" for p in pols)
    polt = (f"<div class=card><h3>Policies ({len(pols)})</h3>"
            f"<table><tr><th>Policy</th><th>Owner</th><th>Geltungsbereich</th><th>Status</th><th>Letztes Update</th></tr>{prow}</table></div>"
            if pols else "<div class=card><h3>Policies (0)</h3><span class=gap>—</span></div>")

    # Strategie — Owner · Status · letztes Update
    strat = [o for o, x in objs.items() if x["fm"].get("type") == "strategy" and tid in (x["fm"].get("concerns") or [])]
    srow = "".join(f"<tr><td><a href='{s}.html'>{dname(s)}</a></td><td>{who_link(objs[s]['fm'].get('owner'))}</td>"
                   f"<td>{stat(s)}</td><td class=dim>{html.escape(str(objs[s]['fm'].get('stand','—')))}</td></tr>" for s in strat)
    strt = (f"<div class=card><h3>Strategie ({len(strat)})</h3>"
            f"<table><tr><th>Strategie</th><th>Owner</th><th>Status</th><th>Letztes Update</th></tr>{srow}</table></div>"
            if strat else "")
    steer = strt + mass + polt

    # Lücken & offene Punkte: aggregiert aus Thema + allen verbundenen Objekten
    related = [tid] + targets_ids + (fm.get("has_kpi") or []) + inis + iros + pols + strat
    gaps = ""
    for oid2 in dict.fromkeys(related):
        for p in (objs.get(oid2, {}).get("fm", {}).get("offene_punkte") or []):
            gaps += f"<tr><td>{name_link(oid2)}</td><td>{html.escape(str(p))}</td></tr>"
    n_gaps = gaps.count("<tr>")
    luecken = (f"<div class=card><h3>Lücken &amp; offene Punkte ({n_gaps})</h3>"
               + (f"<table><tr><th>Objekt</th><th>Offener Punkt</th></tr>{gaps}</table>"
                  if gaps else "<span class='badge ok'>keine offenen Punkte</span>") + "</div>")

    # ---- „Braucht Ihre Aufmerksamkeit" — priorisierte Handlungsliste (Fokus oben) ----
    items = []
    for (t, gap, fc, z, tf) in off_targets:
        det = f" Prognose {fmt(fc[1])} {einh(tf)} ggü. Ziel {fmtnum(z)}{(' (' + gap + ')') if gap else ''}." if fc else "."
        items.append(("bad", f"<b>{dname(t)}</b> ist <b>gefährdet</b> —{det} Verantwortlich: {who_link(tf.get('owner'))}."))
    for i in iros:
        if str(objs[i]['fm'].get('wesentlich', '')).lower() in ('ja', 'true') and not addressers.get(i):
            nr = html.escape(str(objs[i]['fm'].get('iro_nr', i)))
            items.append(("bad", f"Wesentliche {typ_word(i)} <b>{nr}</b> ist noch nicht durch Strategie, Policy oder Ziel gesteuert."))
    if miss_freigabe:
        names = ", ".join(dname(t) for t in miss_freigabe[:3]) + ("…" if len(miss_freigabe) > 3 else "")
        items.append(("warn", f"{len(miss_freigabe)} von {len(targets_ids)} Zielen ohne formale Freigabe: {names}"))
    if miss_risiko:
        items.append(("warn", f"{len(miss_risiko)} Ziele ohne dokumentierte Risikobewertung."))
    if n_gaps:
        items.append(("warn", f"{n_gaps} offene Detailpunkte — siehe „Lücken &amp; offene Punkte“ unten."))
    n_red = sum(1 for c, _ in items if c == "bad")
    if n_red:
        acls = "bad"; head = f"⚠ Handlungsbedarf — {n_red} kritische{'r' if n_red == 1 else ''} Punkt{'e' if n_red != 1 else ''}"
    elif items:
        acls = "warn"; head = "Weitgehend auf Kurs — einige offene Punkte"
    else:
        acls = "ok"; head = "✓ Auf Kurs — keine offenen Aktionen"
    li = "".join(f"<li class={c}>{t}</li>" for c, t in items) or \
        "<li>Alle wesentlichen IROs gesteuert · alle Ziele auf Kurs · keine offenen Punkte.</li>"
    attn = f"<div class='attn {acls}'><div class=attn-h>{head}</div><ul>{li}</ul></div>"

    # ---- Scorecard (Kennzahlen auf einen Blick) ----
    avg = round(sum(mats) / len(mats)) if mats else 0
    c_avg = "ok" if avg >= 75 else ("warn" if avg >= 50 else "bad")
    c_iro = "ok" if n_open == 0 else "bad"
    c_trk = "ok" if off_track == 0 else "bad"
    c_gap = "ok" if n_gaps == 0 else "warn"
    c_gov = "ok" if (strat and pols) else "warn"
    n_total = on_track + off_track
    tiles = (
        f"<div class=tiles>"
        f"<div class='tile {c_avg}' title='Ø Vollständigkeit des Steuerungsapparats über alle Ziele (8 Pflichten je Ziel)'><div class=n>{avg}%</div><div class=l>Steuerungsreife · {len(targets_ids)} Ziele</div></div>"
        f"<div class='tile {c_iro}' title='Wesentliche Auswirkungen/Risiken/Chancen ohne Strategie, Policy oder Ziel'><div class=n>{n_open}</div><div class=l>IROs ungesteuert</div></div>"
        f"<div class='tile {c_trk}' title='Laut Trend/Prognose auf Zielkurs'><div class=n>{on_track}/{n_total}</div><div class=l>Ziele auf Kurs</div></div>"
        f"<div class='tile {c_gap}' title='Dokumentierte offene Punkte über alle verbundenen Objekte'><div class=n>{n_gaps}</div><div class=l>offene Punkte</div></div>"
        f"<div class='tile {c_gov}' title='Vorhandene Strategie- und Policy-Objekte zum Thema'><div class=n>{len(strat)}·{len(pols)}</div><div class=l>Strategie · Policies</div></div>"
        f"</div>")
    return attn + tiles + cov + targets + kpis + steer + luecken


if __name__ == "__main__":
    main()
