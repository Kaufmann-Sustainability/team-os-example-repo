---
id: kpi-scope3-intensitaet
type: kpi
owner: person-sophiewagner
status: vorlaeufig
stand: 2026-06-09
review_zyklus: P3M
vertraulichkeit: intern
esrs_bezug: E1-6
quelle: sustainability-development/carbon-data/inventory/ghg-inventory-2025.md
einheit: kgCO2e/t Produkt
# Beziehungen
sourced_from: [../../sustainability-development/carbon-data/inventory/ghg-inventory-2025.md]
at_risk_from: [finding-2026-05-12-spend-based-overcount]
---

# KPI: Scope-3-Intensität

Treibhausgas-Intensität der Wertschöpfungskette je Tonne produziertes Produkt.
Backing-Daten im Inventar (System of Record bleibt das Carbon-Tool/Inventar — dieses
Objekt **referenziert**, es dupliziert die Zahlen nicht).

## Werte
- **Baseline:** 1.000 kgCO₂e/t (2024).
- **2025:** *noch nicht final berechnet* — Produktionsmenge ausstehend. Absolut sank
  Scope 3 laut Inventar 340.000 → 332.000 tCO₂e (−2,4 %); die Intensität folgt nach
  Vorliegen der Produktionsmenge. (Platzhalter, bewusst nicht erfunden.)
- **Datenqualität:** niedrig — Kat. 1 überwiegend spend-based.

## ⚠ Offenes Risiko
`finding-2026-05-12-spend-based-overcount`: Doppelzählung in der spend-based-Methode
verfälscht **Baseline und laufenden Wert**. Bis zur Korrektur ist dieser KPI als
*vorläufig* markiert — und jede Aufgabe, die auf ihm aufsetzt (Target-Setting,
Reporting), erbt dieses Risiko über die `at_risk_from`-Kante.
