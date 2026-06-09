# Das OS lebendig halten (Maintenance & Beiträge)

> Ein Team OS ist nur so gut wie sein aktuellster Stand. Ein „geteiltes Gehirn", das niemand füttert, wird in Wochen wertlos. Dieses Dokument legt fest, *wie* der Stand erhalten bleibt.

## Das Grundprinzip

**Der Kontext wird dort aktualisiert, wo die Arbeit passiert — nicht in einer separaten „Doku-Runde".** Wer eine Initiative vorantreibt, pflegt ihren Eintrag. Doku ist Teil der Arbeit, nicht eine Aufgabe danach.

## Ownership

Jeder Ordner hat eine:n Owner (siehe `owner:`-Felder bzw. die Kopfzeilen der Dokumente). Faustregel:

| Bereich | Owner-Rolle |
|---------|-------------|
| `programs/strategy/`, Roadmap, Wesentlichkeit | Head of Sustainability |
| `programs/briefs/` | Jeweilige:r Initiativen-Owner |
| `carbon-data/` (Inventar, Faktoren) | Carbon Accounting |
| `implementation/` | Jeweilige:r Plan-Owner |
| `reporting/` | ESG-Reporting Lead |
| `programs/regulatory/` | Sustainability Counsel |
| Root-`CLAUDE.md`, `team/` | Head of Sustainability |

## Wann wird aktualisiert? (Auslöser, nicht Kalender)

Statt „einmal im Quartal alles durchgehen" — an konkrete Ereignisse koppeln:

| Auslöser | Was aktualisieren |
|----------|-------------------|
| Neue Initiative startet | Brief anlegen + `initiative-*`-Objekt unter `object-model/objects/` + Objekt-Kanten setzen |
| Initiative ändert Status | `status:` im `initiative-*`-Objekt + Meilensteine im Brief |
| Neue/aktualisierte Emissionsfaktoren | `ef-*`-Objekt unter `object-model/objects/` |
| Inventar neu berechnet | `carbon-data/inventory/` + ggf. Basisjahr-Hinweis |
| Datenproblem entdeckt | Neues `data-quality-findings/`-Dokument |
| Reporting-Zyklus abgeschlossen | `reporting/` + Retro in `team/retros/` |
| Person kommt/geht | Root-`CLAUDE.md` (Roster) + ggf. Owner-Felder |

## So fügst du eine neue Initiative hinzu (Schritt für Schritt)

1. **Brief schreiben:** Neuer Ordner unter `programs/briefs/<initiative-name>/` mit `<initiative-name>-brief.md`. Nutze das Template-Schema aus `programs/briefs/CLAUDE.md` (Problem · Ziel & Metrik · Scope · Hebel · Abhängigkeiten · Reporting-Bezug · Owner · Meilensteine).
2. **Als Objekt anlegen:** Neues `initiative-*.md`-Objekt unter `object-model/objects/` — mit Objekt-Kanten auf Brief, geplanten Plan, betroffene Faktoren, ESRS-Datenpunkte, Stakeholder, Tickets, `status:`.
3. **Umsetzungsplan (wenn es losgeht):** `implementation/plans/<säule>/<name>.md`, verlinkt zurück auf den Brief.
4. **Daten anbinden:** Betroffene Emissionsfaktoren als `ef-*`-Objekte unter `object-model/objects/` ergänzen/markieren; Inventar-Bezug herstellen.
5. **Reporting-Bezug:** Falls offenlegungsrelevant, in `reporting/esrs-datapoint-mapping.md` ergänzen.

## Konventionen (damit es konsistent bleibt)

- **Jeder Ordner hat ein `CLAUDE.md`** als Wegweiser — was liegt hier, wohin führt es weiter. Neuer Ordner → neues `CLAUDE.md`.
- **Relative Links** zwischen Dokumenten (keine absoluten Pfade), damit Navigation und Forks funktionieren.
- **Die Objekt-Kanten sind die Wahrheit über Verknüpfungen.** Wenn zwei Dinge zusammengehören, werden sie über Kanten zwischen den Objekten unter `object-model/objects/` verbunden.
- **Platzhalter klar markieren** (z. B. „(Stub)", „(Platzhalter)") — damit niemand erfundene Zahlen für echte hält.
- **Datumsformat** in Dateinamen: `YYYY-MM-DD` (z. B. Findings), chronologisch sortierbar.

## Optionale Automatisierung (später)

Wenn das OS produktiv genutzt wird, lohnt sich:
- **SessionStart-Hook** — lädt bei jeder KI-Session automatisch den Root-Kontext (siehe die `session-start-hook`-Anleitung).
- **Link-Check in CI** — prüft bei jedem Commit, dass keine relativen Links ins Leere zeigen.
- **Schema-Check** für die Objekte unter `object-model/objects/` (via `object-model/`-Validator gegen das Schema) — stellt sicher, dass neue Objekte alle Pflichtfelder haben.

Sag Bescheid, wenn einer dieser Bausteine eingerichtet werden soll.
