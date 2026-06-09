# Review-Findings: Struktureller Aufbau des Sustainability OS

> **Zweck:** Backlog der strukturellen (architektonischen) Schwächen des OS-Aufbaus — bewusst getrennt von inhaltlichen Nordmark-Platzhaltern. Entstanden im Review durch Testfragen an das OS.
>
> **Reviewer:** dk (Kaufmann) · **Stand:** 2026-06-09 · **Status:** Review läuft — Liste wächst noch, Priorisierung folgt.

## Querschnitts-Thema

Fast alle Punkte fallen unter ein Dach: **strukturierte Metadaten + Single Source of Truth + Konsistenz-Automatisierung.** Das ist der größte prinzipielle Hebel.

## Findings

| # | Finding | Schwere | Status |
|---|---------|---------|--------|
| 1 | Keine Single Source of Truth (Index & Zahlen doppelt) | Hoch | Offen |
| 2 | Metadaten im Fließtext statt strukturierte Felder | Hoch | Offen |
| 3 | Begründungen fehlen — nur Ergebnisse gespeichert | Hoch | Offen |
| 4 | Fehlender Artefakt-Typ: Entscheidungen (ADR/RFC) | Mittel | Offen |
| 5 | Taxonomie branchengebunden (nicht generalisierbar) | Mittel | Offen |
| 6 | Kein Vertraulichkeits-/Sensitivitätsmodell | Mittel | Offen |
| 7 | Keine sichtbare Aktualität / kein Verfalls-Signal | Mittel | Offen |
| 8 | Daten-Versionierung / Restatement nicht modelliert | Mittel | Offen |
| 9 | Grenze „OS ↔ Systems of Record" undefiniert | Mittel | Offen |
| 10 | Querverweise manuell & brüchig (keine CI) | Niedrig | Offen |
| 11 | „Strategie" verteilt statt eigenständiges Artefakt | Mittel | Offen |

---

### 1 — Keine Single Source of Truth
**Problem:** `initiative-index.yaml` spiegelt Infos aus Briefs/Plänen (Status, Verknüpfungen); Zahlen (z. B. ~430.000 tCO₂e) stehen in Geschäftskontext, Inventar *und* Roadmap.
**Warum prinzipiell:** Mehrfach gehaltene Wahrheit driftet garantiert; Vertrauen ins OS bricht.
**Fix-Richtung:** Daten leben einmal (Inventar/Katalog), Narrativ referenziert statt kopiert.

### 2 — Metadaten im Fließtext
**Problem:** Owner/Status/Datum/Datenqualität mal in Kopfzeilen, mal im Index, mal nicht (Fuhrpark/PCF ohne Owner — Testfrage unbeantwortbar).
**Warum prinzipiell:** „Wer ist verantwortlich?" / „Was ist veraltet?" sind die häufigsten Fragen ans OS.
**Fix-Richtung:** Standardisierter YAML-Front-Matter auf jedem Artefakt (`owner, status, stand, quelle, review-zyklus, vertraulichkeit`); Owner als Pflichtfeld im Index.

### 3 — Begründungen fehlen
**Problem:** Wesentlichkeitsanalyse nennt „E1 = Hoch", aber das *Warum* steckt in einem anderen Dokument.
**Warum prinzipiell:** Für Assurance und Nachvollziehbarkeit ist das „Warum" der Kernwert.
**Fix-Richtung:** Artefakte tragen ihre Begründung mit sich, nicht nur die Konklusion.

### 4 — Fehlender Artefakt-Typ: Entscheidungen
**Problem:** Es gibt Briefs (Pläne) und Findings (Probleme), aber keinen Ort für *Entscheidungen mit Begründung* (z. B. „market-based-PPA statt RECs", „Net-Zero 2040 statt 2035"). Das Original-Team-OS hatte dafür RFCs.
**Warum prinzipiell:** Genau dieses Wissen bleibt sonst in Köpfen — das OS soll es befreien.
**Fix-Richtung:** `decisions/`-Bereich im ADR-Stil.

### 5 — Taxonomie branchengebunden
**Problem:** Säulen Scope 1&2 / Scope 3 / Reporting passen zu einem Hersteller; Dienstleister/Bank/Beratungsmandat schneiden anders.
**Warum prinzipiell:** Für ein wiederverwendbares Template darf der oberste Schnitt keine Branche unterstellen.
**Fix-Richtung:** Schnitt explizit begründen und als austauschbare Schicht behandeln.

### 6 — Kein Vertraulichkeitsmodell
**Problem:** Lieferantenkonditionen, ungeprüfte Zahlen, Rechtsauslegungen liegen gleichberechtigt „offen".
**Warum prinzipiell:** Eine KI kann Vertrauliches an die falsche Stelle bringen.
**Fix-Richtung:** Sensitivitäts-Stufen im Metadaten-Kopf (`vertraulichkeit: intern|vertraulich`).

### 7 — Keine sichtbare Aktualität
**Problem:** Man sieht einem Dokument nicht an, ob es frisch oder veraltet ist.
**Warum prinzipiell:** Ein „geteiltes Gehirn" ohne Alter verleitet zum Vertrauen auf Veraltetes.
**Fix-Richtung:** `stand` + `review-zyklus` als Pflicht; später automatischer Stale-Check.

### 8 — Daten-Versionierung / Restatement
**Problem:** Inventare werden jährlich neu berechnet, Basisjahr restated — aber keine Konvention für Versionen/Änderungshistorie/Audit-Trail.
**Warum prinzipiell:** Assurance verlangt Nachvollziehbarkeit von Änderungen.
**Fix-Richtung:** Versions-/Restatement-Konvention im `carbon-data/`-Bereich.

### 9 — Grenze OS ↔ Systeme
**Problem:** OS verweist auf SAP/Power BI/CDP, aber „Was lebt hier vs. im System of Record?" ist undefiniert.
**Warum prinzipiell:** Sonst landen Live-Zahlen in Markdown (veralten) oder das OS wird als Datenbank missverstanden.
**Fix-Richtung:** Kurzer Grundsatz „Kontext/Entscheidungen/Definitionen hier — Live-Daten nur verlinkt".

### 10 — Brüchige Querverweise
**Problem:** Relative Links brechen still bei Umbenennung; skaliert schlecht.
**Fix-Richtung:** Link-Check in CI (Idee vorhanden, nicht aktiv).

### 11 — „Strategie" verteilt statt eigenständig
**Problem:** Es gibt kein kanonisches Strategie-Dokument. Die Frage „Was ist unsere Strategie?" musste aus `business-context` + `strategy/CLAUDE.md` + `roadmap` + `programs/CLAUDE.md` zusammengesetzt werden. Zudem unscharfe Grenze „Kontext vs. Strategie".
**Warum prinzipiell:** Häufige Kernfrage ohne kanonische Quelle (Spezialfall von #1).
**Fix-Richtung:** `strategy/sustainability-strategy.md` als bündelndes Artefakt; Kontext und Strategie sauber trennen.

---

## Nächste Schritte (nach Review)

1. Findings priorisieren (dk + Team).
2. Entscheiden: nur strukturelle Konventionen festziehen *oder* Ordnerstruktur überarbeiten.
3. Eine überarbeitete Template-Version ableiten.
