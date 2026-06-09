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
    "discloses","reports","backs","covers","challenges",
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
