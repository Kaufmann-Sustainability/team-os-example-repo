#!/usr/bin/env python3
"""Abfrage-/Test-Werkzeug für den Objektgraphen.

Führt die Context-Packs und Views *aus* (was `*.pack.yaml` deklarativ beschreibt),
damit man Traversierung + Eskalation live sieht. Reine Lese-Operationen.

Befehle:
  pack target-setting <topic-id>     z. B. topic-e1-klima
  pack disclosure     <datapoint-id> z. B. datapoint-e1-6-brutto-thg
  pack dma            <topic-id>      z. B. topic-e3-wasser
  my-work             <person-id>     z. B. person-jonasfischer
  gaps                                wesentliche Themen ohne Ziel
  stale                               überfällige Objekte (Frische)
  stats                               Objekt-/Kantenzahl je Typ

Benötigt: PyYAML.
"""
from __future__ import annotations
import re, sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
OFFEN = {"offen", "open", "vorlaeufig", "entwurf", "eingereicht-zur-validierung"}
GESCHLOSSEN = {"geschlossen", "closed", "behoben", "abgeschlossen", "final", "assured", "beschlossen"}

# bekannte Beziehungs-Kanten (Feld -> ist Liste von ids)
KANTEN = {
    "has_target","has_kpi","has_initiative","has_iro","measured_by","supported_by",
    "approved_by","decided_by","supports","affects","at_risk_from","has_budget",
    "uses_factor","concerns","informed_by","scored_under","based_on","applies",
    "discloses","reports","backs","covers","challenges","addresses","depends_on","plans",
    "for_kpi","underpins","assumes","proposes","tests","remediates","for_initiative",
    "approves","threatens",
}


def load():
    objs = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if not m:
            continue
        d = yaml.safe_load(m.group(1)) or {}
        objs[d.get("id", p.stem)] = d
    return objs


def is_open(o):
    return str(o.get("status", "")).lower() not in GESCHLOSSEN


def out(o):
    return [x for x in (o if isinstance(o, list) else [o])]


def edge(objs, oid, rel):
    """Vorwärts: Objekte, auf die oid via rel zeigt."""
    o = objs.get(oid, {})
    return [objs[t] for t in out(o.get(rel, [])) if t in objs]


def incoming(objs, target_id, rel):
    """Rückwärts: Objekte, deren rel auf target_id zeigt."""
    res = []
    for oid, o in objs.items():
        if target_id in out(o.get(rel, [])):
            res.append(o)
    return res


def line(o, marker=" "):
    extra = ""
    if o.get("type") == "target":
        extra = f"  [{o.get('baseline_wert')}→{o.get('zielwert')} {o.get('einheit')}]"
    elif o.get("type") in ("finding", "audit-finding", "kpi", "disclosure"):
        extra = f"  (status: {o.get('status')})"
    return f"  {marker} {o.get('id'):<42} {o.get('type'):<14}{extra}"


# ---------- PACK: TARGET-SETTING ----------
def pack_target_setting(objs, topic_id):
    print(f"\n# Context-Pack: target-setting  ({topic_id})\n")
    topic = objs.get(topic_id)
    if not topic:
        sys.exit(f"Unbekanntes Topic: {topic_id}")
    print("INCLUDE (minimaler Kontext):")
    print(line(topic, "•"))
    for kpi in edge(objs, topic_id, "has_kpi"):
        print(line(kpi, "•"))
    targets = edge(objs, topic_id, "has_target")
    for t in targets:
        print(line(t, "•"))
        for ini in edge(objs, t["id"], "supported_by"):
            print(line(ini, "  ↳"))
            for b in edge(objs, ini["id"], "has_budget"):
                print(line(b, "    ↳"))
    # ESKALATION: offene Findings auf Baseline/Metrik der Ziele
    esk = {}
    for t in targets:
        for kpi in edge(objs, t["id"], "measured_by"):
            for f in edge(objs, kpi["id"], "at_risk_from"):
                if is_open(f):
                    esk[f["id"]] = f
        for f in edge(objs, t["id"], "at_risk_from"):
            if is_open(f):
                esk[f["id"]] = f
    print("\nESKALATION (immer mitgeliefert, trotz exclude):" if esk else "\nESKALATION: keine offenen Risiken.")
    for f in esk.values():
        print(line(f, "⚠"))
    if esk:
        print("  → Regel: kein Ziel auf kippeliger Baseline bestätigen.")


# ---------- PACK: DISCLOSURE ----------
def pack_disclosure(objs, dp_id):
    print(f"\n# Context-Pack: disclosure  ({dp_id})\n")
    dp = objs.get(dp_id)
    if not dp:
        sys.exit(f"Unbekannter Datenpunkt: {dp_id}")
    print("INCLUDE:")
    print(line(dp, "•"))
    for tp in edge(objs, dp_id, "concerns"):
        print(line(tp, "•"))
    discs = incoming(objs, dp_id, "discloses")
    blockers = {}
    for d in discs:
        print(line(d, "•"))
        for kpi in edge(objs, d["id"], "reports"):
            print(line(kpi, "  ↳"))
            for f in edge(objs, kpi["id"], "at_risk_from"):
                if is_open(f):
                    blockers[f["id"]] = f
        for ev in incoming(objs, d["id"], "backs"):
            print(line(ev, "  ↳"))
        for af in incoming(objs, d["id"], "challenges"):
            if is_open(af):
                blockers[af["id"]] = af
    for ctrl in incoming(objs, dp_id, "covers"):
        print(line(ctrl, "•"))
    print("\nESKALATION / GATE (blockiert 'final'/'assured'):" if blockers else "\nGATE: frei — keine offenen Blocker.")
    for b in blockers.values():
        print(line(b, "⛔"))
    if blockers:
        print("  → Verdikt: Offenlegung bleibt ENTWURF. Nichts veröffentlichen, was du nicht beweisen kannst.")


# ---------- PACK: DMA ----------
def pack_dma(objs, topic_id):
    print(f"\n# Context-Pack: dma  ({topic_id})\n")
    topic = objs.get(topic_id)
    if not topic:
        sys.exit(f"Unbekanntes Topic: {topic_id}")
    print("INCLUDE:")
    print(line(topic, "•"))
    iros = edge(objs, topic_id, "has_iro")
    dissens = {}
    for iro in iros:
        print(line(iro, "•") + f"   [{iro.get('impact_wesentlichkeit')}/{iro.get('finanz_wesentlichkeit')}, wesentlich={iro.get('wesentlich')}]")
        for st in edge(objs, iro["id"], "informed_by"):
            print(line(st, "  ↳"))
            if str(iro.get("wesentlich")).lower() in ("nein", "no", "false"):
                dissens[st["id"]] = st
        for me in edge(objs, iro["id"], "scored_under"):
            print(line(me, "  ↳"))
    for dec in incoming(objs, topic_id, "affects"):
        if dec.get("type") == "decision":
            print(line(dec, "•"))
            for th in edge(objs, dec["id"], "applies"):
                print(line(th, "  ↳"))
    nonmaterial = any(str(i.get("wesentlich")).lower() in ("nein","no","false") for i in iros)
    print("\nESKALATION (nicht-wesentlich → Begründung + Dissens immer mit):" if nonmaterial else "\nESKALATION: Thema wesentlich — kein Ausschluss zu verteidigen.")
    for st in dissens.values():
        print(line(st, "⚠") + "  ← widersprechender Stakeholder-Input")


# ---------- VIEW: MY-WORK ----------
def my_work(objs, pid):
    print(f"\n# View: my-work  ({pid})\n")
    owned = [o for o in objs.values() if o.get("owner") == pid and o.get("type") != "person"]
    if not owned:
        print("  (nichts zugeordnet)")
    for o in sorted(owned, key=lambda x: x.get("type", "")):
        risk = ""
        if out(o.get("at_risk_from", [])):
            risk = "  ⚠ Risiko"
        print(line(o) + risk)


# ---------- GAPS ----------
def gaps(objs):
    print("\n# Lücken-Query: wesentliche Themen ohne Ziel\n")
    found = False
    for o in objs.values():
        if o.get("type") == "topic" and str(o.get("status")).lower() == "wesentlich":
            if not out(o.get("has_target", [])):
                print(line(o, "⚠") + "  ← wesentlich, aber kein has_target (hohl)")
                found = True
    if not found:
        print("  Keine Lücke — alle wesentlichen Themen haben mindestens ein Ziel.")


# ---------- COVERAGE (emergente Konsistenz: jede wesentliche IRO von >=1 Ziel abgedeckt) ----------
def coverage(objs, topic_id):
    print(f"\n# IRO-Abdeckung (Konsistenz)  ({topic_id})\n")
    topic = objs.get(topic_id)
    if not topic:
        sys.exit(f"Unbekanntes Topic: {topic_id}")
    iros = [objs[i] for i in out(topic.get("has_iro", [])) if i in objs]
    material = [i for i in iros if str(i.get("wesentlich")).strip('"').lower() != "nein"]
    targets = [objs[t] for t in out(topic.get("has_target", [])) if t in objs]
    # alle addresses-Kanten auf diese IROs (von Zielen vs. Strategie/Policy)
    by_target = {i["id"]: [] for i in material}
    by_strapol = {i["id"]: [] for i in material}
    for o in objs.values():
        for iid in out(o.get("addresses", [])):
            if iid in by_target:
                (by_target if o.get("type") == "target" else by_strapol)[iid].append(o["id"])
    print(f"Wesentliche IROs: {len(material)} · Ziele: {len(targets)}")
    print("\nAbdeckung je IRO  (✓ Ziel · ◐ nur Strategie/Policy · ⛔ gar nicht):")
    nur_sp, gar = [], []
    for i in material:
        t, sp = by_target[i["id"]], by_strapol[i["id"]]
        if t:
            print(f"  ✓ {i['id']:10} ← {', '.join(t)}")
        elif sp:
            print(f"  ◐ {i['id']:10} ← {', '.join(sp)} (kein Metrik-Ziel)")
            nur_sp.append(i["id"])
        else:
            print(f"  ⛔ {i['id']:10} ← NICHTS")
            gar.append(i["id"])
    orph = [t for t in targets if not out(t.get("addresses", []))]
    print("\nKonsistenz-Befund:")
    print("  ✓ Jede wesentliche IRO ist adressiert."
          if not gar else f"  ⛔ Nicht adressiert: {', '.join(gar)}")
    if nur_sp:
        print(f"  ◐ Nur über Strategie/Policy gemanagt (bewusst? kein Metrik-Ziel): {', '.join(nur_sp)}")
    print("  ✓ Jedes Ziel adressiert mindestens eine IRO."
          if not orph else f"  ⛔ Orphan-Ziel(e): {', '.join(t['id'] for t in orph)}")


# ---------- REIFEGRAD (Vollständigkeits-Vertrag je Target) ----------
# Vertrag = Kern-Pflichten, die ein Target zu einem "vollständig gesteuerten" machen.
# Fehlt etwas, ist es entweder anzulegen ODER als offene_punkte zu markieren.
def _incoming(objs, edge, target_id):
    """Objekte, deren <edge> auf target_id zeigt (Rückwärts-Lookup)."""
    return [o for o in objs.values() if target_id in out(o.get(edge, []))]

def reifegrad(objs, arg):
    obj = objs.get(arg)
    if not obj:
        sys.exit(f"Unbekannte ID: {arg}")
    typ = obj.get("type")
    print(f"\n# Reifegrad: Vollständigkeitsverträge\n")
    if typ == "topic":
        print("## Thema — Apparat (topic-gate)\n")
        _print_full(obj, *_topic_checks(objs, obj))
        sections = [("IROs", "has_iro", _iro_checks), ("KPIs", "has_kpi", _kpi_checks),
                    ("Ziele", "has_target", _target_checks), ("Maßnahmen", "has_initiative", _initiative_checks)]
        for label, edge, fn in sections:
            kids = [objs[k] for k in out(obj.get(edge, [])) if k in objs]
            if not kids:
                continue
            print(f"## {label}  (Detail: reifegrad <id>)\n")
            for k in kids:
                _print_compact(k, fn(objs, k)[0])
            print()
    elif typ in _CHECKS:
        _print_full(obj, *_CHECKS[typ](objs, obj))
    else:
        sys.exit("reifegrad erwartet topic | iro | kpi | target | initiative.")


def _wesentlich(o):
    return str(o.get("wesentlich", "")).lower() in ("ja", "true")

def _addressed(objs, iid):
    return any(iid in out(t.get("addresses", [])) for t in objs.values())


def _target_checks(objs, t):
    tid = t["id"]
    checks = [
        ("Owner gesetzt",          bool(t.get("owner"))),
        ("Baseline+Ziel+Jahr",     all(t.get(f) is not None for f in ("baseline_wert","zielwert","zieljahr"))),
        ("≥1 IRO adressiert",      bool(out(t.get("addresses", [])))),
        ("≥1 KPI misst es",        bool(out(t.get("measured_by", [])))),
        ("≥1 Maßnahme trägt es",   bool(out(t.get("supported_by", [])))),
        ("≥1 Annahme hinterlegt",  bool(_incoming(objs, "underpins", tid))),
        ("Freigabe (approval)",    bool(_incoming(objs, "approves", tid))),
        ("Risiken bewertet",       bool(_incoming(objs, "threatens", tid))),
    ]
    bonus = [("Szenario", bool([o for o in _incoming(objs, "proposes", tid) if o.get("type") == "scenario"]))]
    return checks, bonus


def _initiative_checks(objs, i):
    iid = i["id"]
    checks = [
        ("Owner gesetzt",            bool(i.get("owner"))),
        ("≥1 Target verknüpft",      bool(out(i.get("supports", [])))),
        ("≥1 Budget",                bool(out(i.get("has_budget", [])))),
        ("Freigabe/Status (approval)", bool(_incoming(objs, "approves", iid))),
        ("≥1 Milestone",             bool(_incoming(objs, "for_initiative", iid))),
        ("Abhängigkeiten explizit",  bool(out(i.get("depends_on", [])))),
        ("Risiken bewertet",         bool(_incoming(objs, "threatens", iid))),
    ]
    eco = [o for o in objs.values() if iid in out(o.get("prices", [])) or iid in out(o.get("abates", []))]
    bonus = [("Economics (Kosten-Nutzen)", bool(eco))]
    return checks, bonus


def _iro_checks(objs, o):
    # Konditional: Impact -> Impact-Score; Risk/Opportunity -> Financial-Score.
    ist_impact = str(o.get("iro_typ", "")).startswith("Impact")
    checks = [
        ("Typ + Wesentlichkeit gesetzt", bool(o.get("iro_typ")) and o.get("wesentlich") is not None),
        ("Wertschöpfungsketten-Position", bool(o.get("wertschoepfungskette"))),
        ("Begründung vorhanden",         bool(o.get("begruendung"))),
    ]
    if ist_impact:
        checks.append(("Impact-Score (Ausmaß/Umfang)", bool(o.get("impact_wesentlichkeit"))))
        checks.append(("Tatsächlich/potenziell",       bool(o.get("wirkung_art"))))
    else:
        checks.append(("Financial-Score", bool(o.get("finanz_wesentlichkeit"))))
    if _wesentlich(o):
        checks.append(("Wesentlich → adressiert", _addressed(objs, o["id"])))
    return checks, []


def _kpi_checks(objs, k):
    kid = k["id"]
    checks = [
        ("Owner gesetzt",         bool(k.get("owner"))),
        ("Einheit gesetzt",       bool(k.get("einheit"))),
        ("Definition/Methodik",   bool(k.get("methodik"))),
        ("Baseline",              k.get("baseline_wert") is not None),
        ("≥1 Target misst damit", any(kid in out(t.get("measured_by", [])) for t in objs.values())),
        ("Aktueller Wert (kpi-value)", any(o.get("type") == "kpi-value" and kid in out(o.get("for_kpi", [])) for o in objs.values())),
    ]
    bonus = [("Forecast/Trend", any(o.get("type") in ("forecast", "trend") and kid in out(o.get("for_kpi", [])) for o in objs.values()))]
    return checks, bonus


def _topic_checks(objs, tp):
    tid = tp["id"]
    pol = [o for o in objs.values() if o.get("type") == "policy" and tid in out(o.get("concerns", []))]
    mat = [objs[i] for i in out(tp.get("has_iro", [])) if i in objs and _wesentlich(objs[i])]
    alle_adressiert = bool(mat) and all(_addressed(objs, m["id"]) for m in mat)
    checks = [
        ("Owner gesetzt",        bool(tp.get("owner"))),
        ("≥1 IRO",               bool(out(tp.get("has_iro", [])))),
        ("≥1 Policy",            bool(pol)),
        ("≥1 Target",            bool(out(tp.get("has_target", [])))),
        ("≥1 KPI",               bool(out(tp.get("has_kpi", [])))),
        ("≥1 Maßnahme",          bool(out(tp.get("has_initiative", [])))),
        ("Alle wesentlichen IROs adressiert", alle_adressiert),
    ]
    return checks, []


def _policy_checks(objs, p):
    pid = p["id"]
    checks = [
        ("Owner gesetzt",       bool(p.get("owner"))),
        ("Betrifft ein Thema",  bool(out(p.get("concerns", [])))),
        ("≥1 IRO adressiert",   bool(out(p.get("addresses", [])))),
        ("Geltungsbereich",     bool(p.get("geltungsbereich"))),
        ("Freigabe (approval)", bool(_incoming(objs, "approves", pid))),
    ]
    return checks, []


def _decision_checks(objs, d):
    checks = [
        ("Owner gesetzt",            bool(d.get("owner"))),
        ("Datum + Entscheidung",     bool(d.get("datum")) and bool(d.get("entscheidung"))),
        ("Entscheider (decided_by)", bool(out(d.get("decided_by", [])))),
        ("Begründung",               bool(d.get("begruendung"))),
        ("Betrifft etwas (affects)", bool(out(d.get("affects", [])))),
    ]
    bonus = [("Grundlage (based_on / informed_by)",
              bool(out(d.get("based_on", [])) or out(d.get("informed_by", []))))]
    return checks, bonus


_CHECKS = {"target": _target_checks, "initiative": _initiative_checks,
           "iro": _iro_checks, "kpi": _kpi_checks, "topic": _topic_checks,
           "policy": _policy_checks, "decision": _decision_checks}


def _print_full(obj, checks, bonus):
    erfuellt = sum(1 for _, ok in checks if ok)
    score = round(100 * erfuellt / len(checks))
    bar = "█" * (score // 10) + "░" * (10 - score // 10)
    print(f"  {obj['id']}")
    print(f"  Reifegrad {bar} {score}%  ({erfuellt}/{len(checks)} Kern-Pflichten)")
    for name, ok in checks:
        print(f"      {'✓' if ok else '✗'} {name}")
    for name, ok in bonus:
        print(f"      {'＋' if ok else '·'} {name} (Bonus)")
    for op in obj.get("offene_punkte", []) or []:
        print(f"      ⚠ offen: {op}")
    print()


def _print_compact(obj, checks):
    erfuellt = sum(1 for _, ok in checks if ok)
    score = round(100 * erfuellt / len(checks))
    fehlt = [name for name, ok in checks if not ok]
    op = " ⚠offen" if obj.get("offene_punkte") else ""
    tail = ("   fehlt: " + ", ".join(fehlt)) if fehlt else ""
    print(f"   {score:3d}%  {obj['id']}{tail}{op}")


# ---------- BERICHTSREIFE (Release-Gate vor Offenlegung) ----------
def berichtsreife(objs, topic_id):
    tp = objs.get(topic_id)
    if not tp or tp.get("type") != "topic":
        sys.exit("berichtsreife erwartet ein topic.")
    print(f"\n# Berichtsreife: {topic_id}\n")
    blockers = []
    # 1) Apparat vollständig (topic-gate)
    for name, ok in _topic_checks(objs, tp)[0]:
        if not ok:
            blockers.append(f"Apparat unvollständig: {name}")
    # 2) Datenpunkte des Themas -> jeder braucht eine Offenlegung
    dps = [o for o in objs.values() if o.get("type") == "datapoint" and topic_id in out(o.get("concerns", []))]
    if not dps:
        blockers.append("Keine ESRS-Datenpunkte am Thema modelliert")
    for dp in dps:
        discs = [o for o in objs.values() if o.get("type") == "disclosure" and dp["id"] in out(o.get("discloses", []))]
        if not discs:
            blockers.append(f"Datenpunkt ohne Offenlegung: {dp['id']}")
            continue
        # 3) je Offenlegung: berichtete KPI aktuell, ohne offenes Finding, mit Evidenz
        for disc in discs:
            for kid in out(disc.get("reports", [])):
                kvs = [o["id"] for o in objs.values() if o.get("type") == "kpi-value" and kid in out(o.get("for_kpi", []))]
                if not kvs:
                    blockers.append(f"{disc['id']}: KPI {kid} ohne aktuellen Wert")
                if not any(o.get("type") == "evidence" and set(out(o.get("backs", []))) & set(kvs) for o in objs.values()):
                    blockers.append(f"{disc['id']}: keine Evidenz für KPI {kid}")
                for fnd in [o for o in objs.values() if o.get("type") == "finding"
                            and o.get("status") == "offen" and kid in out(o.get("affects", []))]:
                    blockers.append(f"{disc['id']}: offenes Finding {fnd['id']} betrifft KPI {kid}")
    if blockers:
        print(f"  ⛔ NICHT BERICHTSREIF — {len(blockers)} Blocker:\n")
        for b in blockers:
            print(f"      • {b}")
    else:
        print("  ✅ BERICHTSREIF — Apparat steht, Datenpunkte offengelegt, KPIs aktuell & belegt, keine offenen Findings.")
    print()


# ---------- KPI-STATUS (Zeitreihe: Ist-Werte, Forecast, Trend, Frische) ----------
def kpi_status(objs, topic_id):
    print(f"\n# KPI-Status über Zeit  ({topic_id})\n")
    topic = objs.get(topic_id)
    if not topic:
        sys.exit(f"Unbekanntes Topic: {topic_id}")
    kpis = [objs[k] for k in out(topic.get("has_kpi", [])) if k in objs]
    vals, fcs, trs = {}, {}, {}
    for o in objs.values():
        for k in out(o.get("for_kpi", [])):
            t = o.get("type")
            (vals if t == "kpi-value" else fcs if t == "forecast" else trs if t == "trend" else {}).setdefault(k, []).append(o)
    for kpi in kpis:
        kid = kpi["id"]
        vs = sorted(vals.get(kid, []), key=lambda x: x.get("jahr", 0))
        reihe = "  ".join(f"{v.get('jahr')}:{v.get('wert')}" for v in vs) or "— keine Ist-Werte"
        fc = "  ".join(f"{f.get('jahr')}→{f.get('wert')}" for f in fcs.get(kid, [])) or "—"
        tr = trs.get(kid, [])
        trb = tr[0].get("bewertung") if tr else "—"
        mark = "⏰" if not vs else ("⚠" if any(t.get("bewertung") == "off-track" for t in tr) else "✓")
        print(f"  {mark} {kid}")
        print(f"      Ist: {reihe}   ·   Forecast: {fc}   ·   Trend: {trb}")
    off = [k["id"] for k in kpis if any(t.get("bewertung") == "off-track" for t in trs.get(k["id"], []))]
    nodata = [k["id"] for k in kpis if not vals.get(k["id"])]
    print("\nBefund:")
    print(f"  ⚠ Off-track: {', '.join(off)}" if off else "  ✓ Keine KPI off-track.")
    if nodata:
        print(f"  ⏰ Ohne Ist-Werte (Datenlücke): {', '.join(nodata)}")


# ---------- STALE ----------
def stale(objs):
    print("\n# Frische-Sweep: überfällige Objekte\n")
    heute = date.today()
    n = 0
    for o in objs.values():
        rz, stand = o.get("review_zyklus"), o.get("stand")
        m = re.fullmatch(r"P(\d+)M", str(rz or ""))
        if not m or not stand:
            continue
        y, mo, d = map(int, str(stand).split("-"))
        fm = mo + int(m.group(1))
        faellig = date(y + (fm - 1) // 12, (fm - 1) % 12 + 1, d)
        if faellig < heute:
            print(line(o, "⏰") + f"  fällig {faellig}, owner {o.get('owner')}")
            n += 1
    if not n:
        print(f"  Alles frisch (Stichtag {heute}).")


# ---------- STATS ----------
def stats(objs):
    from collections import Counter
    typen = Counter(o.get("type") for o in objs.values())
    kanten = sum(len(out(o.get(k, []))) for o in objs.values() for k in KANTEN)
    print(f"\n# Graph-Statistik\n\n  Objekte gesamt: {len(objs)}   Kanten gesamt: {kanten}\n")
    for t, c in sorted(typen.items(), key=lambda x: -x[1]):
        print(f"  {t:<16} {c}")


def main():
    objs = load()
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    cmd = a[0]
    if cmd == "pack":
        sub = a[1]
        {"target-setting": pack_target_setting, "disclosure": pack_disclosure, "dma": pack_dma}[sub](objs, a[2])
    elif cmd == "my-work":
        my_work(objs, a[1])
    elif cmd == "coverage":
        coverage(objs, a[1])
    elif cmd == "kpi-status":
        kpi_status(objs, a[1])
    elif cmd == "reifegrad":
        reifegrad(objs, a[1])
    elif cmd == "berichtsreife":
        berichtsreife(objs, a[1])
    elif cmd == "gaps":
        gaps(objs)
    elif cmd == "stale":
        stale(objs)
    elif cmd == "stats":
        stats(objs)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
