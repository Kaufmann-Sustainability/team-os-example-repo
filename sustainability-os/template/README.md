# Sustainability OS — Template (leere Instanz)

Dies ist das **leere, wiederverwendbare Template** des Sustainability OS. Es enthält die komplette
Engine + den ESRS-Pack, aber **keine Kundendaten**. Eine neue Kunden-Instanz entsteht, indem dieses
Verzeichnis kopiert, `instance-config.yaml` ausgefüllt und — startend mit *einem* Thema — schrittweise
mit Inhalt gepflegt wird.

> Entwickelt am Vaillant-Use-Case (`../vaillant-dma-2026/` = befülltes Beispiel). Dieses Template ist
> die saubere Ausgangsbasis ohne Inhalt.

## Die drei Schichten (was hier liegt)

| Schicht | Ordner/Datei | Pro Kunde? |
|---|---|---|
| **Core Engine** (framework-agnostisch, **inkl. Wesentlichkeit/DMA-IRO**) | `object-schema.yaml`, `tools/`, generische Gates (`.claude/skills/` — **im Template enthalten**) | nein — ausgeliefert |
| **Framework-Pack** (Offenlegung) | `reference/esrs-*` (Kataloge, Konzept-Spines) | nein — je Pack ausgeliefert |
| **Kunden-Instanz** | `instance-config.yaml`, `objects/`, `reference/anwendbarkeit-<instanz>-*.yaml`, `reporting/` | **ja — entsteht hier** |

**Warum DMA/IRO im Core ist:** Die Wesentlichkeit definiert den **Scope** — sie sagt, *wofür*
Policies, Ziele, KPIs und Maßnahmen überhaupt gebraucht werden. Jedes Steuerungsobjekt ist an eine
wesentliche IRO verankert. Das gilt für jedes Rahmenwerk; standard-spezifisch ist nur die daraus
folgende **Offenlegung** (= Pack).

## Eine neue Kunden-Instanz aufsetzen

1. Dieses Verzeichnis kopieren → `../<instanz>/` (z. B. `acme-2026/`).
2. `instance-config.yaml` ausfüllen (Firma, Roster, Frameworks, Start-Thema).
3. Onboarding-Flow unten durchlaufen — beginnend mit **einem** Thema.
4. `python3 tools/validate.py` muss grün bleiben (Integrität).

## Onboarding-Flow: ein Thema von „bewertet" zu „gesteuert"

Die Reihenfolge folgt dem Modell **Bewerten → Steuern → Messen → (später) Offenlegen**. Jeder Schritt
läuft über einen Gate-Skill, der Vollständigkeit erzwingt — nichts kommt halbfertig & unmarkiert rein.

```
  1) SCOPE / WESENTLICHKEIT  (Fundament)
     • Thema anlegen (topic-*) und IROs bewerten          → iro-gate
     • wesentliche IROs markieren                          → das definiert den Steuerungsbedarf
     • in instance-config: themen_im_scope + anwendbarkeit-<instanz>-*.yaml füllen

  2) GOVERNANCE / VERANTWORTUNG
     • Roster pflegen (Personen)                           → instance-config.roster
     • Verantwortung wird zugewiesen — nie still           → (Handover/RASCI, in Arbeit)
     • bis dahin: person-unassigned als Platzhalter-Owner

  3) STEUERUNG je wesentlicher IRO
     • Policy                                              → policy-gate
     • Ziel(e) (an IRO verankert)                          → target-gate
     • KPI(s)                                              → kpi-gate
     • Maßnahme(n)/Programm(e)                             → initiative-gate
     • Dach-Check „Thema vollständig gesteuert?"           → topic-gate + iro-coverage

  4) MESSUNG
     • Ist-Werte je KPI über Zeit                          → performance-tracking
     • Annahmen/Risiken hinterlegen                        → assumption-register / target-gate

  5) OFFENLEGUNG  (erst bei Erweiterung, via Framework-Pack)
     • Datenpunkte aus dem Katalog                         → gen_datapoints.py
     • Berichts-Entwurf je Standard/Version                → bericht_entwurf.py
     • Release-Veto vor Offenlegung                        → disclosure-readiness
```

## Werkzeuge (Core)

| Tool | Zweck |
|---|---|
| `tools/validate.py` | referenzielle Integrität (jede Kante zeigt auf existierendes Objekt erlaubten Typs) |
| `tools/query.py` | Abfragen/Views: `reifegrad`, `my-work`, `gaps`, `stale`, `stats` |
| `tools/linkage_guard.py` | findet Steuerungs-Inhalt, der keinen Bericht erreicht (stille Lücken) |
| `tools/graph_html.py` | interaktive Graph-Visualisierung |

## Werkzeuge (ESRS-Pack)

| Tool | Zweck |
|---|---|
| `tools/import_esrs_catalog.py` | EFRAG-/EC-Workbook → versionierter Datenpunkt-Katalog |
| `tools/gen_datapoints.py` | quantitative Katalog-Datenpunkte → Datenpunkt-Objekte (idempotent) |
| `tools/bericht_entwurf.py` | Berichts-Entwurf je Standard & Katalog-Version (stabile Konzepte) |

## Roadmap / bekannte Baustellen

Siehe `../PRODUCT-READINESS.md` (Master-Plan) und die `TODO-*.md`-Notizen im Vaillant-Beispiel:
RASCI/Handover, Dedup, Such-Index, Datentyp-Review, Datenpunkt-Versionsstabilität, sowie die
physische Pack-Trennung + pack-fähige Tools.
