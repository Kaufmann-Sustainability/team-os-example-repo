---
name: measure-planning
description: Maßnahmen/Initiativen für ein Ziel planen — mit verpflichtendem Owner, Budget und verlinkten Dependencies. Einsetzen, wenn Initiativen (`initiative-*`) angelegt oder geändert werden, damit jedes Ziel von mindestens einer Maßnahme getragen wird und jede Maßnahme betreibbar ist (Owner + Budget + Abhängigkeiten explizit).
---

# Skill: Maßnahmen-Planung

Macht ein Ziel **betreibbar**: konkrete Maßnahmen (`initiative`) mit Verantwortung, Mitteln und
Abhängigkeiten. Schließt direkt an `iro-coverage` an (Ziele existieren) und macht aus „Ziel gesetzt"
ein „Ziel wird umgesetzt".

## Pflichtfelder je Maßnahme (`initiative`)
| Feld/Kante | Regel |
|------------|-------|
| `owner` | **Pflicht** — eine reale `person-*`, nicht Platzhalter. (Ohne echten Owner ist es modelliert, nicht gesteuert.) |
| `supports` | ≥1 `target`, auf das die Maßnahme einzahlt |
| `has_budget` | ≥1 `budget`-Objekt (Betrag, Währung, Jahr) — sonst nicht ressourciert |
| `depends_on` | alle `dependency`-Objekte, von denen die Maßnahme abhängt (natürl./sozial/regulatorisch) — explizit verlinken, nicht implizit lassen |
| `status` | geplant / in-umsetzung / abgeschlossen |

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Kein Ziel ohne Maßnahme.** Jedes `target` muss von ≥1 `initiative` via `supports` getragen
  sein — sonst ist es ein Wunsch, kein Plan.
- 🚫 **Keine Maßnahme ohne Owner + Budget.** Beides Pflicht.
- 🔗 **Dependencies explizit machen.** Wenn eine Maßnahme an einer externen Voraussetzung hängt
  (Förderpolitik, CO₂-armer Strom, qualifizierte Belegschaft …), als `depends_on → dependency`
  verlinken. So werden Abhängigkeiten abfragbar statt im Kopf.
- 👥 **Owner echt, nicht Platzhalter.** Ein `person-dma-lead`-Sammelowner ist ein Warnzeichen.

## Vor dem Abschluss
- [ ] Jedes Ziel des Themas hat ≥1 Maßnahme (`supported_by`)
- [ ] Jede Maßnahme: realer Owner, ≥1 Budget, Dependencies verlinkt
- [ ] `validate.py` grün
