# Carbon Data

Die Datenebene des Nachhaltigkeitsteams — das Pendant zu „Analytics". Hier liegt das THG-Inventar, der Emissionsfaktoren-Katalog, die KPI-Definitionen und die Auswertungen.

## Inhalt

| Ordner/Datei | Beschreibung |
|--------------|--------------|
| `inventory/` | THG-Inventar nach Scope/Jahr — die offiziellen Bilanzierungs-Zahlen |
| `emission-factors-catalog.yaml` | Registry aller verwendeten Emissionsfaktoren — Quelle, Einheit, Gültigkeit, Owner |
| `metrics/` | KPI-Definitionen (analog Metrik-Glossar) |
| `queries/` | Wiederkehrende Auswertungen (SQL / Tabellen-Transformationen) |
| `dashboards.md` | Verweise auf Dashboards (z. B. Power BI / internes Carbon-Tool) |

## Datenquellen

| Quelle | Beschreibung | Zugang |
|--------|--------------|--------|
| ERP (SAP) | Aktivitätsdaten: Energieverbrauch, Materialeinkauf, Spend | SAP-Export / Connector |
| Energieabrechnungen | Strom-, Gas-, Wärmeverbrauch je Standort | Versorger-Portale |
| Lieferanten-Fragebögen | Lieferanten-spezifische Primärdaten (Scope 3) | CDP / interne Plattform |
| Emissionsfaktor-DBs | DEFRA, ecoinvent, GEMIS, Versorger-Faktoren | Lizenzierte DBs |

## Kern-KPIs

| KPI | Definition | Ziel |
|-----|------------|------|
| **THG gesamt (tCO₂e)** | Summe Scope 1+2+3 | Reduktionspfad lt. Roadmap |
| **Scope 1+2 absolut** | Direkte + eingekaufte Energie | −42 % bis 2030 (Basis 2024) |
| **Scope 3 Intensität** | tCO₂e / t produziertes Produkt | −25 % bis 2030 |
| **Primärdaten-Abdeckung** | % Scope-3-Kat.-1-Emissionen mit lieferanten-spez. EF | ≥ 60 % bis 2027 |
| **Datenqualitäts-Score** | Anteil Aktivitätsdaten aus Messung vs. Schätzung | steigend |
| **Anteil erneuerbarer Strom** | % market-based EE | 100 % bis 2027 |

## Bilanzierungs-Grundsätze

Nach **GHG Protocol** (siehe `../programs/regulatory/frameworks/frameworks-matrix.md`). Scope 2 dual ausgewiesen (location- + market-based). Basisjahr 2024, Neuberechnung bei strukturellen Änderungen > 5 %.

## Wichtigste Verweise

- Aktuelles Inventar: `inventory/ghg-inventory-2025.md`
- Faktoren-Katalog: `emission-factors-catalog.yaml`
- Datenqualitäts-Findings: `../implementation/data-quality-findings/`
