# Beispiele: Standardisierte Definition & Ziel

Referenz für den erwarteten Detailgrad des `sustainability-standard`-Skills.

## Beispiel — Definition (Modus A)

```markdown
### Scope-2-Emissionen (market-based)
- **Definition:** Indirekte THG-Emissionen aus eingekaufter Energie, bewertet mit den vertraglich beschafften Stromprodukten (z. B. PPA, Herkunftsnachweise) statt mit dem Durchschnitts-Netzmix.
- **Abgrenzung:** Nicht zu verwechseln mit Scope 2 *location-based* (Durchschnitts-Netzfaktor). Beide werden parallel ausgewiesen; nur der market-based-Wert spiegelt Beschaffungsentscheidungen wider.
- **Einheit / Berechnung:** tCO₂e = Strombezug (kWh) × market-based-Faktor (kgCO₂e/kWh, aus `carbon-data/emission-factors-catalog.yaml`)
- **ESRS-Bezug:** E1-5 (Energiemix), E1-6 (Scope 2)
- **Synonyme:** marktbasierter Scope 2
- **Owner:** Sophie Wagner · **Stand:** 2026-06-09
```

## Beispiel — Ziel (Modus B)

```yaml
  - ziel: Grünstrom-Anteil 100 %
    metrik: Anteil erneuerbarer Strom (market-based), %
    baseline_wert: 0
    baseline_jahr: 2024
    zielwert: 100
    zieljahr: 2027
    geltungsbereich: Alle 4 Produktionsstandorte (DE/PL/CZ)
    esrs_bezug: E1-5
    massnahmen_bezug: renewable-electricity-ppa
    owner: Aylin Demir
    status: in Umsetzung
    stand: 2026-06-09
```

## Beispiel — Fundament-Ziel statt hohlem Ziel (Modus B, ohne Baseline)

Wenn jemand „Recyclingquote Prozessschrott um 20 % steigern" für E5 setzen will, aber **keine Baseline** existiert, liefert der Skill stattdessen:

```yaml
  - ziel: Baseline Recyclingquote Prozessschrott erheben
    metrik: Recyclingquote Prozessschrott, %
    baseline_wert: null   # zu erheben
    baseline_jahr: 2026
    zielwert: null        # erst nach Baseline festlegbar
    zieljahr: 2027
    geltungsbereich: Produktionsstandorte
    esrs_bezug: E5-5
    massnahmen_bezug: noch keine
    owner: Tobias Klein
    status: geplant (Fundament)
    stand: 2026-06-09
```
