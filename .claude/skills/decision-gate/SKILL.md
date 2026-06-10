---
name: decision-gate
description: Vollständigkeits-Wächter für Entscheidungen (decision-*). Einsetzen, wenn eine Entscheidung dokumentiert wird — stellt sicher, dass das "Warum" erhalten bleibt: Datum, Entscheidung, Entscheider, Begründung und was sie betrifft. Eine Entscheidung ohne Begründung und Entscheider ist nicht nachvollziehbar und nicht prüfbar.
---

# Skill: Decision-Gate (Vollständigkeits-Vertrag für Entscheidungen)

Entscheidungen sind das institutionelle Gedächtnis: Warum wurde eine Weiche so gestellt? Eine
Entscheidung ist erst *nachvollziehbar*, wenn klar ist, wer sie wann auf welcher Grundlage traf
und was sie berührt. Dieser Skill ist der **Wächter**.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Feld / Kante |
|---|---------|--------------|
| 1 | **Owner** | `owner: person-…` |
| 2 | **Datum + Entscheidung** | `datum:` + `entscheidung:` (was wurde beschlossen?) |
| 3 | **Entscheider** | `decided_by: [person-…]` — wer hat entschieden? |
| 4 | **Begründung** | `begruendung:` — *warum* so? (der Kern; nicht im Fließtext verstecken) |
| 5 | **Betrifft etwas** | `affects: [target / kpi / topic …]` — worauf wirkt sie? |
| + | *Bonus* | `based_on` (Methodik) / `informed_by` (Stakeholder, Szenario) |

## Ablauf
1. `python3 tools/query.py reifegrad <decision-id>`.
2. Begründung und Entscheider ergänzen; `affects`-Kanten auf die berührten Objekte setzen.
3. Wo eine Methodik oder ein Stakeholder-Input zugrunde lag → `based_on` / `informed_by` verlinken.

## Harte Regeln
- 🚫 **Keine Entscheidung ohne Begründung und Entscheider.** Sonst ist sie ein Beschluss ohne Gedächtnis.
- 🔗 **`affects` verlinken statt beschreiben.** Eine Entscheidung, die nirgends andockt, ist im Graph unsichtbar und wirkungslos.
- 🧭 **Provenienz-Brücke:** Entscheidungen, die auf Annahmen beruhen, sollten über `informed_by`/`based_on` dorthin zeigen (→ `assumption-register`).

## Vor dem Abschluss
- [ ] `reifegrad <decision>` 100 % **oder** offene Pflicht in `offene_punkte`
- [ ] `affects` zeigt auf alle real berührten Objekte
- [ ] `validate.py` grün
