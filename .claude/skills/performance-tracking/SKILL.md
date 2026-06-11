---
name: performance-tracking
description: KPI-Fortschritt über Zeit pflegen — Ist-Werte (kpi-value) je Jahr, Forecast und Trend (on-/off-track). Einsetzen, wenn neue Messwerte vorliegen oder geprüft wird, ob ein Ziel auf Kurs ist — damit jede aktive KPI eine laufende Werte-Reihe hat und Abweichungen sichtbar werden, statt erst beim Reporting aufzufallen.
---

# Skill: Performance-Tracking (KPI über Zeit)

Macht aus einem statischen Baseline→Zielwert eine **lebende Zeitreihe**. Jede aktive KPI bekommt
je Berichtsjahr einen `kpi-value`; ein `forecast` projiziert den Pfad; ein `trend` bewertet
on-track / off-track gegen den Zielwert.

## Ablauf
1. **Ist-Wert erfassen.** Neues `kpi-value`-Objekt: `for_kpi: [kpi-…]`, `jahr`, `wert`. (ID-Schema
   `kpi-value-<kpi>-<jahr>` → idempotent, kein Duplikat je Jahr.)
2. **Forecast aktualisieren.** `forecast` mit Zieljahr-Projektion bei aktuellem Tempo.
3. **Trend bewerten.** `trend` mit `bewertung: on-track | off-track | watch`, abgeleitet aus
   Werte-Reihe vs. Zielpfad (`target.baseline_wert → zielwert@zieljahr`).
4. **Prüfen.** `python3 tools/query.py kpi-status <topic-id>`.

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Keine aktive KPI ohne aktuellen Ist-Wert.** Fehlt der `kpi-value` fürs laufende
  Berichtsjahr → Datenlücke, nachtragen (oder Owner anstoßen).
- ⏱️ **Trend muss zur Werte-Reihe passen.** „on-track" nur, wenn der Forecast den Zielwert
  erreicht — sonst `off-track`/`watch`.
- 🔁 **Off-track ist ein Auslöser, kein Etikett.** Bei `off-track` → `measure-planning`
  (zusätzliche Maßnahme) oder eine `recommendation` erzeugen. (Beispiel: `trend-e1-scope3-11`
  off-track → Handlungsbedarf sichtbar.)
- 🔗 Werte sollten über `evidence` (`backs → kpi-value`) belegt sein (siehe `assurance`-Skill).

## Vor dem Abschluss
- [ ] Jede aktive KPI des Themas hat einen `kpi-value` fürs aktuelle Jahr
- [ ] Trend-Bewertung konsistent mit Forecast vs. Zielpfad
- [ ] Off-track-KPIs haben eine Folge-Maßnahme/Empfehlung
- [ ] `validate.py` grün
