# Onboarding: Carbon Accounting Analyst

Ergänzt das [allgemeine Onboarding](onboarding-general.md). Fokus: THG-Bilanzierung nach GHG Protocol.

## Was du besitzt

- Das **THG-Inventar** (`../../sustainability-development/carbon-data/inventory/`) — die offiziellen Zahlen.
- Die **Emissionsfaktoren** als `ef-*`-Objekte (`../../object-model/objects/`) — Pflege, Quellen, Gültigkeit.
- **Datenqualität** — Plausibilisierung, Findings (`../../sustainability-development/implementation/data-quality-findings/`).

## Mentales Modell

```
Aktivitätsdaten (kWh, t, €)  ×  Emissionsfaktor (kgCO2e/Einheit)  =  Emission (tCO2e)
        ↑ aus ERP/Zählern              ↑ aus den ef-*-Objekten
```

Scope 2 immer **dual** (location- + market-based). Scope 3 priorisiert nach Beitrag — Genauigkeit folgt Wesentlichkeit (Kat. 1 zuerst).

## Erste fachliche Reads

1. [Carbon Data — Übersicht](../../sustainability-development/carbon-data/CLAUDE.md)
2. [THG-Inventar 2025](../../sustainability-development/carbon-data/inventory/ghg-inventory-2025.md)
3. [GHG-Protocol/Rahmenwerke](../../sustainability-development/programs/regulatory/frameworks/frameworks-matrix.md)
4. Beispiel-Finding: [spend-based Doppelzählung](../../sustainability-development/implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md)

## Erste Aufgaben

- [ ] Einen Emissionsfaktor von der Quelle bis ins Inventar nachverfolgen
- [ ] Eine Scope-2-Position location- vs. market-based nachrechnen
- [ ] Mit Jonas (Lieferketten) den Scope-3-Datenfluss durchsprechen
