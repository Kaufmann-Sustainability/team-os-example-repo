---
name: iro-coverage
description: Sicherstellen, dass jede WESENTLICHE IRO eines Themas durch ≥1 KPI ABGEBILDET ist (ESRS-Pflicht, Kante iro→measured_by→kpi) und sichtbar machen, welche IROs zusätzlich durch Ziele/Policies/Strategie GESTEUERT werden (optional). Einsetzen, wenn ein Thema von „bewertet" zu „messbar/gesteuert" gebracht wird, oder wenn sich IROs/KPIs/Ziele ändern — damit keine wesentliche IRO unmessbar bleibt.
---

# Skill: IRO-Abdeckung (Messung zuerst, Steuerung optional)

Dieser Skill bringt ein Thema von **bewertet → messbar → (optional) gesteuert**. Ausgangslage:
ein Topic mit seinen IROs (aus der DMA). Es gibt **zwei Achsen** mit unterschiedlicher Verbindlichkeit:

| Achse | Kante | Verbindlichkeit |
|-------|-------|-----------------|
| **Messung** | `iro → measured_by → kpi` | 🔴 **Pflicht (ESRS).** Jede wesentliche IRO wird durch ≥1 KPI abgebildet. |
| **Steuerung** | `target / strategy / policy → addresses → iro` | ◐ **Optional, getrackt.** „Keine" ist eine gültige, zu begründende Antwort. |

Beide sind **many-to-many**: ein KPI kann mehrere IROs abbilden, eine IRO mehrere KPIs haben;
ein Ziel deckt oft mehrere IROs ab. Die IRO→KPI-Zuordnung wird als `decision` dokumentiert
(wer/wann/warum) — `decision.affects: [iro, kpi]` + `begruendung` (→ `decision-gate`).

> Komponiert mit `kpi-gate` (KPI-Vertrag), `sustainability-standard` (Baseline-Disziplin je Ziel)
> und `measure-planning` (Maßnahmen mit Owner/Budget/Dependencies).

## Ablauf
1. **IROs sichten.** Lies `topic-*.md → has_iro`; filtere die **wesentlichen** (`wesentlich: ja`).
   Gruppiere sie nach Management-Logik (z. B. „Use-Phase", „eigene Emissionen", „Vorkette",
   „Finanzrisiken/Chancen").
2. **Messen — Pflicht.** Pro IRO ≥1 KPI bestimmen und die Kante `measured_by: [kpi, …]` in der
   **IRO-Datei** setzen (die KPI selbst folgt `kpi-gate`). Ein KPI darf mehrere IROs eines Clusters
   abbilden. Die Zuordnung als `decision` dokumentieren.
3. **Steuern — optional.** Wo sinnvoll, ein `target` (mit `addresses: [iro, …]`), eine `policy`
   und/oder eine `strategy` aufsetzen. Wo bewusst nichts gesteuert wird: das ist erlaubt und wird
   im `coverage`-Report als ◐ ausgewiesen — nicht als Fehler.
4. **Prüfen.** `python3 tools/query.py coverage <topic-id>` ausführen.

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Keine wesentliche IRO ohne KPI.** Jede `wesentlich: ja`-IRO braucht ≥1 `measured_by`-KPI.
  Fehlt sie, ist das eine ESRS-Lücke → schließen oder als `offene_punkte` mit Datum begründen.
- ◐ **Steuerung ist optional, aber sichtbar.** Ob eine IRO ein Ziel/eine Policy hat, trackt der
  `coverage`-Report (✓ gesteuert · ◐ nur gemessen, nicht gesteuert) — „nur gemessen" ist gültig.
- 🚫 **Kein Orphan-Ziel.** Wenn ein `target` existiert, muss es ≥1 IRO über `addresses` adressieren.
- 🧭 Baseline/Einheit/Zieljahr je Ziel nach `sustainability-standard`.

## Vor dem Abschluss
- [ ] `query.py coverage <topic>` → „Jede wesentliche IRO ist durch ≥1 KPI abgebildet."
- [ ] Jede IRO→KPI-Zuordnung durch eine `decision` (Begründung) belegt
- [ ] Steuerungs-Lücken (◐) bewusst bestätigt; kein Orphan-Ziel
- [ ] `validate.py` grün
