# Nordmark — Sustainability Team OS

In-house Nachhaltigkeitsfunktion der **Nordmark Industrie GmbH** (fiktives Beispielunternehmen). Diese Datei ist der Einstiegspunkt: Sie liefert Team-Roster, Kommunikationskanäle, einen Doc-Index und die Terminologie, mit der jede KI-Session startet.

> **Hinweis:** Alle Namen, IDs, Zahlen und Ziele sind Platzhalter und dienen nur der Demonstration der Struktur.

## Unternehmenskontext (Kurzfassung)

Nordmark Industrie GmbH — mittelständischer Industriezulieferer (Metallverarbeitung), ~2.800 Mitarbeitende, 4 Produktionsstandorte (DE, PL, CZ). CSRD-pflichtig ab Geschäftsjahr 2025. **North Star:** Net-Zero bis 2040 entlang der gesamten Wertschöpfungskette, mit SBTi-validierten Near-Term-Zielen für 2030. Volle Geschäftskontext-Doku: `sustainability-development/programs/strategy/business-context/company-sustainability-context.md`.

## Team

| Funktion | Name | GitHub | Tool-ID (Linear/Jira) | Slack ID |
|----------|------|--------|----------------------|----------|
| Head of Sustainability (CSO) | Dr. Lena Hartmann | `lenahartmann` | `a1b2c3d4-0001` | `U0SUS001` |
| ESG-Reporting Lead | Markus Bauer | `markusbauer` | `a1b2c3d4-0002` | `U0SUS002` |
| Carbon Accounting Analyst | Sophie Wagner | `sophiewagner` | `a1b2c3d4-0003` | `U0SUS003` |
| Carbon Accounting Analyst | Tobias Klein | `tobiasklein` | `a1b2c3d4-0004` | `U0SUS004` |
| Decarbonization Program Manager | Aylin Demir | `aylindemir` | `a1b2c3d4-0005` | `U0SUS005` |
| Supplier Sustainability Lead | Jonas Fischer | `jonasfischer` | `a1b2c3d4-0006` | `U0SUS006` |
| Sustainability Data Analyst | Mira Schulz | `miraschulz` | `a1b2c3d4-0007` | `U0SUS007` |
| Sustainability Communications | Clara Voss | `claravoss` | `a1b2c3d4-0008` | `U0SUS008` |
| Sustainability Counsel (Regulatorik) | Dr. Felix Brandt | `felixbrandt` | `a1b2c3d4-0009` | `U0SUS009` |

## Slack-Kanäle

| Kanal | ID | Sichtbarkeit | Zweck |
|-------|-----|--------------|-------|
| #nachhaltigkeit-team | `C0SUS001` | Privat | Team-weite Abstimmung, Entscheidungen, Wochenplanung |
| #esg-reporting | `C0SUS002` | Privat | CSRD/ESRS-Reporting, Offenlegung, Assurance-Abstimmung |
| #carbon-accounting | `C0SUS003` | Privat | THG-Bilanzierung, Emissionsfaktoren, Datenqualität |
| #dekarbonisierung | `C0SUS004` | Privat | Maßnahmen, Reduktionsprojekte, Roadmap-Tracking |
| #lieferketten-esg | `C0SUS005` | Privat | Lieferanten-Engagement, Scope-3, Sorgfaltspflichten (LkSG/CSDDD) |
| #nachhaltigkeit-allgemein | `C0SUS006` | Öffentlich | Unternehmensweite Updates, Awareness, Erfolge |
| #csrd-projekt | `C0SUS007` | Privat | CSRD-Erstanwendungs-Projekt, Gap-Analyse, Datenpunkte |
| #klima-alerts | `C0SUS008` | Privat | Automatische Alerts: Datenpipelines, Faktoren-Updates, Schwellwerte |

### DM-Gruppen

| Gruppe | Mitglieder | ID | Zweck |
|--------|-----------|-----|-------|
| Sustainability Leads | Lena, Markus, Aylin | `G0SUS001` | Strategische Steuerung, Priorisierung |
| Carbon Crew | Sophie, Tobias, Mira | `G0SUS002` | Bilanzierungs-Detailfragen, Faktoren, Datenmodell |
| Reporting + Legal | Markus, Felix, Clara | `G0SUS003` | Offenlegungs-Wording, Regulatorik, Assurance |

## Doc-Index

**Wenn du Artefakte zu einer bestimmten Initiative suchst (Briefs, Pläne, Faktoren, Inventar, Reporting-Datenpunkte, Tickets), schau zuerst in `sustainability-development/initiative-index.yaml`.** Dort ist jede Initiative auf all ihre zugehörigen Artefakte gemappt.

| Bereich | Datei | Beschreibung |
|---------|-------|--------------|
| Initiative-Index | `sustainability-development/initiative-index.yaml` | Master-Lookup — jede Initiative → Briefs, Pläne, Faktoren, Inventar, Reporting, Tickets |
| Sustainability Development | `sustainability-development/CLAUDE.md` | Dachordner für alle Nachhaltigkeits-Artefakte |
| Programme | `sustainability-development/programs/CLAUDE.md` | Strategie, Roadmaps, Initiativen-Briefs, Regulatorik, Stakeholder, Meetings |
| Strategie | `sustainability-development/programs/strategy/CLAUDE.md` | Net-Zero-Strategie, Roadmaps, Wesentlichkeitsanalyse, Geschäftskontext |
| Briefs | `sustainability-development/programs/briefs/CLAUDE.md` | Initiativen-Briefs (das „PRD" der Nachhaltigkeit) |
| Regulatorik | `sustainability-development/programs/regulatory/CLAUDE.md` | Rahmenwerke & Standards: CSRD/ESRS, GHG Protocol, SBTi, GRI, TCFD, LkSG/CSDDD |
| Stakeholder | `sustainability-development/programs/stakeholders/CLAUDE.md` | Interne Fachbereiche, Lieferanten, Investoren, Auditoren — Routing-Tabelle |
| Carbon Data | `sustainability-development/carbon-data/CLAUDE.md` | THG-Inventar, Emissionsfaktoren-Katalog, KPIs, Queries, Dashboards |
| Implementation | `sustainability-development/implementation/CLAUDE.md` | Umsetzungspläne für Reduktionsmaßnahmen + Datenqualitäts-Findings |
| Reporting | `sustainability-development/reporting/CLAUDE.md` | Offenlegung, ESRS-Datenpunkt-Mapping, Assurance-Vorbereitung |
| Team | `team/CLAUDE.md` | Onboarding-Guides und Team-Ressourcen |

## Terminologie

| Begriff | Definition |
|---------|------------|
| Scope 1 | Direkte Emissionen aus eigenen/kontrollierten Quellen (Verbrennung, Fuhrpark, Prozesse) |
| Scope 2 | Indirekte Emissionen aus eingekaufter Energie (Strom, Wärme) — location- und market-based |
| Scope 3 | Alle übrigen indirekten Emissionen der Wertschöpfungskette (15 Kategorien lt. GHG Protocol) |
| THG / GHG | Treibhausgase, ausgewiesen in tCO₂e (CO₂-Äquivalente) |
| Emissionsfaktor (EF) | Umrechnungswert von Aktivitätsdaten (z. B. kWh, t Stahl) in tCO₂e |
| Aktivitätsdaten | Messbare Mengen, die mit einem EF multipliziert die Emission ergeben |
| CSRD | Corporate Sustainability Reporting Directive — EU-Berichtspflicht |
| ESRS | European Sustainability Reporting Standards — die Standards unter der CSRD |
| Doppelte Wesentlichkeit | Bewertung nach Impact- *und* finanzieller Wesentlichkeit (ESRS-Pflicht) |
| SBTi | Science Based Targets initiative — Validierung wissenschaftsbasierter Ziele |
| Datenpunkt | Eine konkrete ESRS-Offenlegungsanforderung (z. B. E1-6 Brutto-THG) |
| LkSG / CSDDD | Lieferkettensorgfaltspflichtengesetz / EU Corporate Sustainability Due Diligence Directive |
| PPA | Power Purchase Agreement — langfristiger Grünstrom-Liefervertrag |
