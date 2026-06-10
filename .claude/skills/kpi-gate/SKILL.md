---
name: kpi-gate
description: Vollständigkeits-Wächter für Kennzahlen (kpi-*). Einsetzen, wenn eine KPI angelegt oder geändert wird — stellt sicher, dass sie definiert (Einheit + Methodik), verankert (misst ein Target), bezifferbar (Baseline) und lebendig (aktueller Wert) ist. Eine KPI ohne Methodik oder ohne aktuellen Wert ist keine Kennzahl, sondern eine Überschrift.
---

# Skill: KPI-Gate (Vollständigkeits-Vertrag für Kennzahlen)

Eine KPI ist erst eine *Kennzahl*, wenn man weiß: wie sie gerechnet wird, welches Ziel sie misst,
woher sie kommt (Baseline) und wo sie heute steht. Dieser Skill ist der **Wächter**.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Feld / Kante |
|---|---------|--------------|
| 1 | **Owner** | `owner: person-…` |
| 2 | **Einheit** | `einheit:` |
| 3 | **Definition/Methodik** | `methodik:` — wie genau wird gerechnet? (→ `sustainability-standard`) |
| 4 | **Baseline** | `baseline_wert` + `baseline_jahr` |
| 5 | **Misst ein Target** | ein `target` mit `measured_by: [diese KPI]` — wofür existiert die Zahl? |
| 6 | **Aktueller Wert** | ein `kpi-value` mit `for_kpi: [diese KPI]` fürs laufende Jahr (→ `performance-tracking`) |
| + | *Bonus* | `forecast` / `trend` (Pfad & on-/off-track) |

## Ablauf
1. `python3 tools/query.py reifegrad <kpi-id>` (oder `kpi-status <topic-id>` für die Zeitreihe).
2. Methodik/Baseline ergänzen; aktuellen `kpi-value` anlegen (oder Datenlücke als `offene_punkte` markieren).
3. Forecast/Trend über `performance-tracking` ergänzen.

## Harte Regeln
- 🚫 **Keine KPI ohne Methodik.** Eine Zahl ohne Berechnungsweg ist nicht prüfbar und nicht reproduzierbar.
- 🔗 **Keine KPI ohne Target.** Eine Kennzahl, die kein Ziel misst, ist Selbstzweck → mit `measured_by` verankern oder löschen.
- ⏰ **Keine aktive KPI ohne aktuellen Wert.** Fehlt der `kpi-value` fürs laufende Jahr → Datenlücke, markieren (vgl. `performance-tracking`).
- 📐 Einheit konsistent zur Methodik und zum Target (gleiche Einheit wie das gemessene Ziel).

## Vor dem Abschluss
- [ ] `reifegrad <kpi>` 100 % **oder** jede offene Pflicht in `offene_punkte`
- [ ] Einheit von KPI und gemessenem Target stimmen überein
- [ ] `validate.py` grün
