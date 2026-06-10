#!/usr/bin/env python3
"""
Zuordnungs-Wächter — fängt Inhalt, der STILL aus dem Bericht fällt.

Standard-agnostisch: prüft ALLE wesentlichen Themen (topic-* mit status: wesentlich)
quer über E1–E5, S1–S4, G1, ES — nicht nur Klima. Frage je Standard:
  „Erreicht die Steuerungs-Inhalt (target/policy/initiative/kpi) überhaupt einen
   Berichts-Entwurf, oder verschwindet er lautlos?"

Erreichbarkeit (identisch zur Logik in bericht_entwurf.py):
  - MANUELL    : Objekt steht in einem datapoint.satisfied_by.
  - ABGELEITET : Objekt matcht eine Tier-1-Regel (esrs-concepts*.yaml -> ableitung)
                 eines Standards, der eine Konzept-Spine hat.
Alles andere = VERWAIST -> würde in keinem Entwurf auftauchen.

Zwei Befund-Klassen:
  [ZUORDNUNG]  Standard HAT eine Spine, aber Inhalt ist nicht verlinkt  -> FEHLER (exit 1).
               Das ist die echte stille Lücke (z. B. neue KPI ohne satisfied_by).
  [STRUKTUR]   Wesentlicher Standard hat noch GAR KEINE Spine/Katalog   -> WARNUNG.
               Bekannter Backlog (nur E1 ist heute modelliert), kein Regress.

Aufruf:  python3 tools/linkage_guard.py
Benötigt: PyYAML.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
STD = re.compile(r"^(e[1-5]|s[1-4]|g1|es)$")          # ESRS-Standard-Token
CONTENT = {"target", "policy", "initiative", "kpi"}    # Steuerungs-Inhalt, der berichtet wird


def load_objects():
    out = {}
    for p in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(p.read_text(encoding="utf-8"))
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            out[fm.get("id", p.stem)] = fm
    return out


def std_of(oid):
    parts = oid.split("-")
    return parts[1] if len(parts) > 1 and STD.match(parts[1]) else None


def load_spines():
    spines = {}
    for p in sorted((ROOT / "reference").glob("esrs-concepts*.yaml")):
        sp = yaml.safe_load(open(p))
        s = str(sp.get("standard", "")).lower()
        if s:
            spines[s] = sp
    return spines


def main():
    objs = load_objects()
    spines = load_spines()

    # wesentliche Themen je Standard
    material = {}
    for oid, fm in objs.items():
        if fm.get("type") == "topic" and str(fm.get("status", "")).lower() == "wesentlich":
            s = std_of(oid)
            if s:
                material.setdefault(s, []).append(oid)

    # manuell verlinkte IDs (über alle datapoints)
    manual = set()
    for fm in objs.values():
        if fm.get("type") == "datapoint":
            manual.update(fm.get("satisfied_by", []) or [])

    def derivable(oid, fm):
        s = std_of(oid)
        sp = spines.get(s)
        if not sp:
            return False
        for r in sp.get("ableitung", []):
            if fm.get("type") == r["typ"] and any(
                str(x).startswith(r["praefix"]) for x in fm.get(r["feld"], []) or []
            ):
                return True
        return False

    # Inhalt je Standard einordnen
    per_std = {}  # std -> {"reach": [], "orphan": []}
    for oid, fm in objs.items():
        if fm.get("type") not in CONTENT:
            continue
        s = std_of(oid)
        if not s:
            continue
        bucket = per_std.setdefault(s, {"reach": [], "orphan": []})
        if oid in manual or derivable(oid, fm):
            bucket["reach"].append(oid)
        else:
            bucket["orphan"].append(oid)

    # --- Report ---
    mats = sorted(material)
    print("ZUORDNUNGS-WÄCHTER — Erreichbarkeit von Steuerungs-Inhalt in den Bericht")
    print(f"{len(mats)} Standards mit wesentlichen Themen · "
          f"Spine vorhanden: {sorted(spines)} \n")
    print(f"  {'Std':<4} {'wes.Themen':>10} {'Spine':>6} {'Inhalt':>7} {'erreichb.':>9} {'verwaist':>9}")
    fail_orphans, struct_gap = [], []
    for s in mats:
        b = per_std.get(s, {"reach": [], "orphan": []})
        n_content = len(b["reach"]) + len(b["orphan"])
        has_spine = s in spines
        if has_spine:
            n_orphan = len(b["orphan"])
            if n_orphan:
                fail_orphans.append((s, b["orphan"]))
        else:
            # ohne Spine ist ALLES unerreichbar -> struktureller Backlog
            n_orphan = n_content
            if n_content:
                struct_gap.append((s, n_content))
        flag = "✅" if has_spine and not b["orphan"] else ("⚠" if not has_spine else "❌")
        print(f"  {s.upper():<4} {len(material[s]):>10} {('ja' if has_spine else '—'):>6} "
              f"{n_content:>7} {len(b['reach']):>9} {n_orphan:>9}  {flag}")

    if fail_orphans:
        print("\n❌ [ZUORDNUNG] Inhalt in modelliertem Standard, der in KEINEN Entwurf fließt:")
        for s, ids in fail_orphans:
            print(f"   {s.upper()}: {len(ids)} verwaist")
            for i in ids[:12]:
                print(f"     - {i}  ({objs[i].get('type')})  → kein satisfied_by, keine Ableitungsregel")
            if len(ids) > 12:
                print(f"     … +{len(ids)-12} weitere")
        print("   Fix: datapoint.satisfied_by setzen ODER eine Ableitungsregel in der Spine ergänzen.")

    if struct_gap:
        total = sum(n for _, n in struct_gap)
        print(f"\n⚠ [STRUKTUR] {len(struct_gap)} wesentliche Standards ohne Konzept-Spine/Katalog "
              f"→ {total} Inhalts-Objekte noch nicht berichtsfähig (bekannter Backlog):")
        for s, n in struct_gap:
            print(f"   {s.upper()}: {len(material[s])} wes. Themen, {n} Inhalts-Objekte — Spine fehlt")
        print("   Fix: je Standard reference/esrs-concepts-<std>.yaml + Katalog anlegen (wie E1).")

    print()
    if fail_orphans:
        print("FEHLER: stille Zuordnungs-Lücke in modelliertem Standard.")
        return 1
    print("✓ Keine stille Zuordnungs-Lücke in modellierten Standards"
          + (f" ({sum(n for _,n in struct_gap)} Objekte im Struktur-Backlog, s. o.)." if struct_gap else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
