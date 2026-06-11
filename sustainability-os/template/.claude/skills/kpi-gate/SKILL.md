---
name: kpi-gate
description: Vollständigkeits-Wächter für Kennzahlen (kpi-*). Einsetzen, wenn eine KPI angelegt oder geändert wird — stellt sicher, dass sie definiert (Einheit + Methodik), verankert (bildet ≥1 IRO ab), bezifferbar (Baseline) und lebendig (aktueller Wert) ist. Eine KPI ohne Methodik oder ohne aktuellen Wert ist keine Kennzahl, sondern eine Überschrift.
---

# Skill: KPI-Gate (Vollständigkeits-Vertrag für Kennzahlen)

Eine KPI ist erst eine *Kennzahl*, wenn man weiß: wie sie gerechnet wird, **welche IRO sie abbildet**,
woher sie kommt (Baseline) und wo sie heute steht. Dieser Skill ist der **Wächter**.

> **Verankerung (ESRS-Logik):** Der harte Anker einer KPI ist die **IRO**, nicht das Ziel.
> ESRS verlangt, dass jede wesentliche IRO durch ≥1 Kennzahl abgebildet wird (Kante
> `iro → measured_by → kpi`) — *ob* daraus ein Ziel, eine Policy oder eine Maßnahme wird, ist
> frei. Eine KPI darf zusätzlich ein Ziel messen (`target → measured_by → kpi`); das ist nützlich
> für die interne Steuerung, aber **optional**.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Feld / Kante |
|---|---------|--------------|
| 1 | **Owner** | `owner: person-…` |
| 2 | **Einheit** | `einheit:` |
| 3 | **Definition/Methodik** | `methodik:` — wie genau wird gerechnet? (→ `sustainability-standard`) |
| 4 | **Baseline** | `baseline_wert` + `baseline_jahr` |
| 5 | **Bildet ≥1 IRO ab** | eine `iro` mit `measured_by: [diese KPI]` — *was* macht diese Zahl messbar? |
| 6 | **Aktueller Wert** | ein `kpi-value` mit `for_kpi: [diese KPI]` fürs laufende Jahr (→ `performance-tracking`) |
| + | *Bonus* | misst ein `target` (`measured_by`, interne Steuerung) · `forecast` / `trend` |

## Ablauf
1. `python3 tools/query.py reifegrad <kpi-id>` (oder `kpi-status <topic-id>` für die Zeitreihe).
2. Methodik/Baseline ergänzen; die IRO(s) per `measured_by` auf diese KPI verankern; aktuellen
   `kpi-value` anlegen (oder Datenlücke als `offene_punkte` markieren).
3. Forecast/Trend über `performance-tracking` ergänzen.

## Harte Regeln
- 🚫 **Keine KPI ohne Methodik.** Eine Zahl ohne Berechnungsweg ist nicht prüfbar und nicht reproduzierbar.
- 🔗 **Keine KPI ohne IRO-Bezug.** Eine Kennzahl, die keine IRO abbildet, ist Selbstzweck → von ≥1
  IRO über `measured_by` verankern (die IRO-Datei trägt die Kante) oder löschen.
- ◐ **Ein Ziel zu messen ist optional.** Fehlt der Target-Bezug, ist das keine Lücke — die KPI
  steht direkt für die IRO. Vorhanden = Bonus (interne Steuerung sichtbar).
- ⏰ **Keine aktive KPI ohne aktuellen Wert.** Fehlt der `kpi-value` fürs laufende Jahr → Datenlücke, markieren (vgl. `performance-tracking`).
- 📐 Einheit konsistent zur Methodik (und, falls vorhanden, zum gemessenen Ziel).

## Vor dem Abschluss
- [ ] `reifegrad <kpi>` 100 % **oder** jede offene Pflicht in `offene_punkte`
- [ ] ≥1 IRO verankert die KPI über `measured_by`
- [ ] `validate.py` grün
