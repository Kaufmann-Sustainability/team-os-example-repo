# THG-Inventar 2025

**Berichtsjahr:** 2025 · **Basisjahr:** 2024 · **Methodik:** GHG Protocol Corporate Standard · **Owner:** Sophie Wagner · **Status:** Vorläufig (Assurance Q1 2027)

## Gesamtübersicht (tCO₂e)

| Scope | 2024 (Basis) | 2025 | Δ vs. Basis | Methodik |
|-------|-------------|------|-------------|----------|
| Scope 1 | 38.000 | 36.500 | −3,9 % | Aktivitätsdaten × EF (Erdgas, Diesel) |
| Scope 2 (location-based) | 50.000 | 48.000 | −4,0 % | Verbrauch × Netzfaktor |
| Scope 2 (market-based) | 52.000 | 41.000 | −21,2 % | PPA Tranche 1 wirksam |
| Scope 3 | 340.000 | 332.000 | −2,4 % | gemischt (siehe unten) |
| **Gesamt (market-based)** | **430.000** | **409.500** | **−4,8 %** | |

## Scope 3 nach Kategorie

| Kat. | Beschreibung | tCO₂e 2025 | Methodik | Datenqualität |
|------|--------------|-----------|----------|---------------|
| 1 | Eingekaufte Güter (Stahl/Alu) | 210.000 | überwiegend spend-based | niedrig → Verbesserung läuft |
| 4 | Transport & Distribution (upstream) | 48.000 | distanzbasiert | mittel |
| 11 | Nutzung verkaufter Produkte | 52.000 | Annahmen-basiert | niedrig |
| Übrige | Kat. 2,3,5,6,7,9 | 22.000 | gemischt | gemischt |

## Wichtige Hinweise

- **Scope 2 market-based** sinkt deutlich durch PPA Tranche 1 (`../../programs/briefs/renewable-electricity-ppa/`). Location-based bleibt nahezu konstant — der echte Reduktionseffekt ist im market-based-Wert sichtbar.
- **Scope 3 Kat. 1** dominiert und ist methodisch schwach (spend-based). Verbesserung über Lieferanten-Engagement (`../../programs/briefs/scope-3-supplier-engagement/`). Achtung Doppelzählungs-Risiko beim Methodenwechsel: `../../implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md`.
- Verwendete Faktoren: die `ef-*`-Objekte unter `../../../object-model/objects/`.

## Reporting-Bezug

Dieses Inventar speist **ESRS E1-6** (Brutto-THG je Scope). Mapping: `../../reporting/esrs-datapoint-mapping.md`.
