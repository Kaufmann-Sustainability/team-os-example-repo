---
name: initiative-gate
description: Vollständigkeits-Wächter für Maßnahmen (initiative-*). Einsetzen, wenn eine Initiative angelegt oder geändert wird — stellt sicher, dass sie betreibbar UND verankert ist: mit Target-Bezug, Owner, Budget, Freigabe, Milestones, Dependencies und bewerteten Risiken (oder explizit als offener Punkt markiert). Erweitert measure-planning um Freigabe/Ausführung/Risiko. Keine Maßnahme ohne Ziel.
---

# Skill: Initiative-Gate (Vollständigkeits-Vertrag für Maßnahmen)

Eine Maßnahme ist erst dann *steuerbar*, wenn klar ist: welches Ziel sie bedient, wem sie gehört,
woraus sie finanziert ist, wer sie freigegeben hat, welche Meilensteine sie hat, wovon sie abhängt
und was ihre Umsetzung gefährdet. Dieser Skill ist der **Wächter**: Er lässt eine Maßnahme rein,
aber **nie still unvollständig** — jede Lücke ist gefüllt oder als `offene_punkte` markiert.

Er baut auf `measure-planning` (Owner + Budget + Dependencies) auf und ergänzt die fehlenden
Spuren: **Freigabe, Ausführung (Milestones), Risiko** und — als Vorgriff — **Economics**.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Umsetzung |
|---|---------|-----------|
| 1 | **Verantwortung (RASCI)** | `owner: person-…` = **Accountable** (genau einer) · **≥1 `responsible: [person-…]`** (führt die Umsetzung aus — bei Maßnahmen oft eine *andere* Stelle als die Accountable, z. B. Werkleitung). Owner-Wechsel nur über ein `handover` — **nie still**. |
| 2 | **≥1 Target** | `supports: [target-…]` — **welches Ziel bedient sie?** Die nicht verhandelbare Invariante: keine Maßnahme ohne Ziel |
| 3 | **≥1 Budget** | `has_budget: [budget-…]` — woraus finanziert? (→ `measure-planning`) |
| 4 | **Freigabe/Status** | ein `approval` mit `approves: [diese initiative]` (Gremium + Datum + Genehmiger) |
| 5 | **≥1 Milestone** | ein `milestone` mit `for_initiative: [diese initiative]` — wie wird Fortschritt verankert? |
| 6 | **Dependencies** | `depends_on: [dependency-…]` — wovon hängt die Umsetzung ab? (→ `measure-planning`) |
| 7 | **Risiken bewertet** | ≥1 `risk` mit `threatens: [diese initiative]` — was kann die Umsetzung kippen? |
| + | *Bonus* | **Economics** (Kosten-Nutzen / ROI / €-pro-t-CO₂ → `economics`-Skill), Evidenz |

> **Risk ≠ IRO.** Ein Umsetzungs-Risiko (Lieferengpass, Fachkräftemangel, Genehmigungsstau) ist
> ein eigenes `risk`-Objekt mit `threatens`, **keine** DMA-Wesentlichkeits-IRO.

## Ablauf
1. **Vertrag prüfen:** `python3 tools/query.py reifegrad <initiative-id>` (oder `<topic-id>` für alle Maßnahmen).
2. **Lücken schließen** — fehlendes Objekt anlegen (Approval, Milestone, Risk, Budget …) und verlinken.
3. **Was (noch) nicht geht, markieren:** als `offene_punkte:`-Liste ins Front-Matter der Initiative.
4. **Erneut prüfen** bis Reifegrad 100 % **oder** jede Restlücke ein bewusster `offene_punkt` ist.

## Harte Regeln
- 🚫 **Keine Maßnahme ohne `supports → target`.** Eine Initiative ohne Ziel ist Aktivität ohne Zweck → blockieren oder Ziel verlinken.
- 🚫 **Keine stille Lücke.** Punkt 4–7 fehlen? → anlegen *oder* `offene_punkte`. Nie weglassen.
- ✅ **`status: in-umsetzung` braucht eine `approval`.** Umsetzung ohne Freigabe ist ein Widerspruch → markieren.
- 🔗 **Risiken & Meilensteine verlinken statt beschreiben.** Im Fließtext zählt es nicht; es braucht `risk`-/`milestone`-Objekte.
- 💶 **Ohne Kosten-Nutzen ist Priorisierung blind.** Fehlt Economics, ist es ein offener Punkt, bis der `economics`-Skill greift.

## Vor dem Abschluss
- [ ] `reifegrad <initiative>` zeigt 100 % **oder** jede offene Pflicht steht in `offene_punkte`
- [ ] Jede Maßnahme hat mindestens ein `supports → target`
- [ ] Approval-Genehmiger ≠ Owner (Funktionstrennung) bei echten Freigaben
- [ ] `validate.py` grün

> Drittes Objekt-Gate nach `target-gate` — gleiche Schablone (Vertrag, `reifegrad`-Check,
> `offene_punkte`-Marker). Es bleiben `iro-gate`, `kpi-gate`, `topic-gate`.
