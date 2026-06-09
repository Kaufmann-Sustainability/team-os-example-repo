# Stakeholder

Das Pendant zu „Customers": Ein Nachhaltigkeitsteam hat keine zahlenden Kunden, aber dieselbe Dynamik — **interne und externe Parteien, deren Anforderungen, Daten und Beziehungen gepflegt werden müssen.** Diese Datei ist die Routing-Tabelle.

## Struktur

Jeder Stakeholder hat einen Ordner unter `accounts/<name>/` mit Kontext, Anforderungen und Interaktions-Notizen (analog zu Kundengesprächs-Notizen).

## Stakeholder-Register

| Stakeholder | Typ | Ordner | Was sie von uns brauchen / wir von ihnen |
|-------------|-----|--------|------------------------------------------|
| Procurement / Einkauf | Intern | `accounts/procurement/` | CO₂ ins Vergabe-Scoring; liefern Spend- & Lieferantendaten |
| Finance / Controlling | Intern | `accounts/finance-controlling/` | Reporting-Integration, PPA-Freigabe; liefern Finanzdaten für CSRD |
| Lieferant: ACME Stahl | Extern | `accounts/lieferant-acme-stahl/` | Primärdaten-EFs, Reduktionscommitment; größter Stahllieferant |
| Ökostrom-Anbieter Helion | Extern | `accounts/oekostrom-anbieter-helion/` | PPA-Konditionen, Herkunftsnachweise |
| Wirtschaftsprüfer (Assurance) | Extern | `accounts/wirtschaftspruefer-assurance/` | Prüfspur, Datenpunkt-Nachweise für limited assurance |
| Investoren / Hausbanken | Extern | `accounts/investoren-hausbanken/` | ESG-Rating, Sustainability-Linked-Loan-KPIs |

## Hinweis

Stakeholder-Input fließt direkt in die Wesentlichkeitsanalyse (`../strategy/materiality/double-materiality-assessment-2026.md`) und in einzelne Initiativen-Briefs (`../briefs/`).

*(In diesem Scaffold sind die `accounts/`-Ordner als Platzhalter angelegt; pro Stakeholder käme hier ein `CLAUDE.md` plus Interaktions-Notizen.)*
