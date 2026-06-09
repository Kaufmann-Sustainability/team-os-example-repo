---
id: disclosure-e1-6-2025
type: disclosure
owner: person-markusbauer
status: entwurf
stand: 2026-06-09
review_zyklus: P3M
vertraulichkeit: intern
esrs_bezug: E1-6
esrs_datapoint: E1-6
berichtsjahr: 2025
version: "0.3-entwurf"
quelle: sustainability-development/carbon-data/inventory/ghg-inventory-2025.md
# Beziehungen
discloses: [datapoint-e1-6-brutto-thg]
reports: [kpi-scope3-intensitaet]
---

# Offenlegung E1-6 — Berichtsjahr 2025 (Entwurf v0.3)

Der **versionierte Berichtstext** (Grundproblem C / Finding #19 — bisher gänzlich
unmodelliert). Das ist der Wortlaut, der in den Lagebericht geht — als Objekt mit
`version` und `berichtsjahr`, nicht als verstreute Word-Datei.

## Berichtstext (Entwurf)
> Die Brutto-Treibhausgasemissionen der Nordmark Industrie GmbH betrugen 2025
> **409.500 tCO₂e** (Scope 1: 36.500; Scope 2 market-based: 41.000; Scope 3: 332.000).
> Gegenüber dem Basisjahr 2024 (430.000 tCO₂e) entspricht das einer Reduktion von 4,8 %.
> Scope 3 (eingekaufte Güter) bleibt mit ~81 % der dominierende Anteil.

## ⚠ Warum noch Entwurf, nicht final
Diese Offenlegung kann **nicht final werden**, solange zwei Dinge offen sind — beide
liefert der Disclosure-Pack über die Eskalations-Klausel automatisch mit:
1. `kpi-scope3-intensitaet` ist **vorläufig** (offene Finding `finding-2026-05-12-spend-based-overcount`
   verfälscht Scope-3-Kat.-1 und die Baseline 2024).
2. `audit-finding-2026-baseline-konsistenz`: Der Prüfer hat **Basisjahr↔Berichtsjahr-Konsistenz**
   beanstandet — genau wegen derselben Doppelzählung.

> **Der eigentliche Beweis des Spikes:** *Eine* Tatsache (die kippende Baseline) taucht in
> **drei** Aufgaben auf — Target-Setting, und jetzt Disclosure — weil alle zum selben
> KPI-Objekt traversieren. Objekt existiert einmal, Kontext ist verbunden.
