# Sustainability Development

Alle Nachhaltigkeits-Artefakte der Nordmark Industrie GmbH — Programme/Strategie, Carbon Data, Umsetzung und Reporting.

## Doc-Index

| Pfad | Beschreibung |
|------|--------------|
| [programs/CLAUDE.md](programs/CLAUDE.md) | Strategie, Roadmaps, Initiativen-Briefs, Regulatorik, Stakeholder, Prozesse, Meetings |
| [carbon-data/CLAUDE.md](carbon-data/CLAUDE.md) | THG-Inventar, Emissionsfaktoren-Katalog, KPI-Glossar, Queries, Dashboards |
| [implementation/CLAUDE.md](implementation/CLAUDE.md) | Umsetzungspläne für Reduktionsmaßnahmen, Datenqualitäts-Findings |
| [reporting/CLAUDE.md](reporting/CLAUDE.md) | CSRD/ESRS-Offenlegung, Datenpunkt-Mapping, Assurance-Vorbereitung |
| [../object-model/](../object-model/) | Objektmodell — Initiativen liegen als `initiative-*.md`-Objekte vor und sind über Objekt-Kanten auf Brief, Plan, Faktoren, Inventar, Reporting-Datenpunkte, Tickets verknüpft |

## Mapping zum klassischen Team OS

Diese Struktur adaptiert das Forge-„Team OS". Für alle, die das Original kennen:

| Forge (Produkt-Team) | Hier (Nachhaltigkeits-Team) |
|----------------------|------------------------------|
| `product/PRDs/` | `programs/briefs/` — Initiativen-Briefs |
| `product/strategy/roadmaps/` | `programs/strategy/roadmaps/` — Net-Zero-Roadmap |
| `product/competitive-research/` | `programs/regulatory/` — Rahmenwerke & Standards |
| `product/customers/` | `programs/stakeholders/` — interne/externe Stakeholder |
| `analytics/` + `data-catalog.yaml` | `carbon-data/` + `ef-*`-Objekte unter `../object-model/objects/` |
| `engineering/plans/` + `bug-investigations/` | `implementation/plans/` + `data-quality-findings/` |
| `feature-index.yaml` | `initiative-*`-Objekte + Objekt-Kanten unter `../object-model/objects/` |
