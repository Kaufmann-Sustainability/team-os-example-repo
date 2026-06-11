---
name: policy-gate
description: Vollständigkeits-Wächter für Policies (policy-*). Einsetzen, wenn eine ESRS-Policy angelegt oder geändert wird — stellt sicher, dass sie ein Thema betrifft, mindestens eine IRO adressiert, einen Geltungsbereich nennt, einen Owner hat und formal freigegeben ist. ESRS verlangt je wesentlichem Thema eine Policy — dieses Gate sorgt dafür, dass sie mehr ist als eine Überschrift.
---

# Skill: Policy-Gate (Vollständigkeits-Vertrag für Policies)

ESRS verlangt je wesentlichem Thema eine Policy. Eine Policy ist erst *belastbar*, wenn sie an
ein Thema und konkrete IROs gebunden ist, ihren Geltungsbereich nennt und formal beschlossen wurde.
Dieser Skill ist der **Wächter**.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Feld / Kante |
|---|---------|--------------|
| 1 | **Owner** | `owner: person-…` |
| 2 | **Betrifft ein Thema** | `concerns: [topic-…]` |
| 3 | **≥1 IRO adressiert** | `addresses: [iro-…]` — *welche* Impacts/Risks/Opportunities steuert sie? |
| 4 | **Geltungsbereich** | `geltungsbereich:` — für wen/was gilt sie? (Konzern, Standorte, Produktlinien) |
| 5 | **Freigabe** | ein `approval` mit `approves: [diese policy]` (Gremium + Datum) |

## Ablauf
1. `python3 tools/query.py reifegrad <policy-id>`.
2. Fehlende IRO-Bezüge ergänzen (eine Policy „im Allgemeinen" ohne IRO-Anker ist wertlos).
3. Geltungsbereich präzisieren, Freigabe als `approval` anlegen — oder Lücke als `offene_punkte` markieren.

## Harte Regeln
- 🚫 **Keine Policy ohne IRO-Bezug.** `concerns: topic` allein genügt nicht — sie muss über `addresses` an konkreten Hebeln hängen, sonst ist sie nicht prüfbar.
- 🏛️ **Keine in-kraft-Policy ohne Freigabe.** `status: in-kraft` ohne `approval` ist ein Widerspruch → markieren.
- 🔗 **Konsistenz mit der Steuerung:** Die IROs, die die Policy adressiert, sollten auch durch Ziele adressiert sein (→ `iro-coverage`). Policy ohne Ziel = Absicht ohne Umsetzung.

## Vor dem Abschluss
- [ ] `reifegrad <policy>` 100 % **oder** offene Pflicht in `offene_punkte`
- [ ] Adressierte IROs sind auch durch Ziele gedeckt (`iro-coverage`)
- [ ] `validate.py` grün
