---
name: topic-gate
description: Vollständigkeits-Wächter für Themen (topic-*). Einsetzen, wenn ein wesentliches Thema von "bewertet" zu "gesteuert" gebracht wird — prüft, ob der volle Steuerungs-Apparat steht: IROs, Policy, Targets, KPIs, Maßnahmen, Owner UND dass jede wesentliche IRO adressiert ist. Das Dach-Gate, das die anderen vier zusammenfasst.
---

# Skill: Topic-Gate (Vollständigkeits-Vertrag für Themen)

Ein wesentliches Thema ist erst *gesteuert*, wenn der ganze Apparat steht: bewertete IROs, eine
Policy, messbare Ziele, lebende KPIs, tragende Maßnahmen — und kein wesentlicher Hebel bleibt
unadressiert. Dieses Gate ist das **Dach**; es bündelt `iro-gate`, `target-gate`, `kpi-gate`,
`initiative-gate` und `iro-coverage` zu einer Thema-Vollständigkeit.

## Der Vertrag (Apparat-Pflichten)
| # | Pflicht | Prüfung |
|---|---------|---------|
| 1 | **Owner** | `owner: person-…` |
| 2 | **≥1 IRO** | `has_iro` — die Wesentlichkeitsanalyse liegt vor |
| 3 | **≥1 Policy** | eine `policy` mit `concerns: [dieses topic]` (ESRS verlangt Policy je wesentlichem Thema) |
| 4 | **≥1 Target** | `has_target` |
| 5 | **≥1 KPI** | `has_kpi` |
| 6 | **≥1 Maßnahme** | `has_initiative` |
| 7 | **Alle wesentlichen IROs adressiert** | jede IRO mit `wesentlich: ja` hat ein `target`, das sie `addresses` (→ `iro-coverage`) |

## Ablauf (Dashboard)
1. `python3 tools/query.py reifegrad <topic-id>` → zeigt den **Apparat** oben und darunter
   kompakte Roll-ups für IROs, KPIs, Ziele, Maßnahmen (mit „fehlt: …" je Objekt).
2. Schwächste Objekte zuerst: das jeweilige Objekt-Gate ziehen (`reifegrad <id>` für Detail).
3. Apparat-Lücken (fehlende Policy, unadressierte IRO) schließen oder als `offene_punkte` am Thema markieren.

## Harte Regeln
- 🚫 **Kein wesentliches Thema ohne Policy + Target + KPI + Maßnahme.** Das ist der ESRS-Minimal-Apparat.
- 🎯 **Keine wesentliche IRO ohne Steuerung.** Punkt 7 ist der Kern der doppelten Wesentlichkeit — eine bewertete, aber unadressierte IRO ist ein Compliance-Loch.
- 🪆 **Thema vollständig ⇏ Objekte vollständig.** Der Apparat kann stehen, während einzelne Ziele/IROs Lücken haben — die Roll-ups zeigen beides. Beides muss grün werden.

## Vor dem Abschluss
- [ ] `reifegrad <topic>` — Apparat 100 % **oder** offene Punkte am Thema vermerkt
- [ ] Roll-ups: kein Objekt mit unmarkierter Lücke (sonst dessen Gate ziehen)
- [ ] `validate.py` grün

> Fünftes und letztes Objekt-Gate. Zusammen mit `iro/target/kpi/initiative-gate` deckt die
> Wächter-Schicht jetzt die ganze Steuerungskette ab — von der Bewertung bis zur Umsetzung.
