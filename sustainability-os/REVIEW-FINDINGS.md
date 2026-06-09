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
| 12 | Fehlender zeitlich gerahmter Jahresprogramm-/Planungs-Layer | Mittel | Offen |
| 13 | Stakeholder-Ansprechpersonen nicht strukturiert; Accounts uneinheitlich befüllt | Mittel | Offen |
| 14 | Kein Record durchgeführter Maßnahmen (Aktivitäts-/Done-Log fehlt) | Hoch | Offen |
| 15 | Wesentliche Themen außer E1 nicht operationalisiert (Daten-/Ziel-Lücke) | Hoch | Offen |
| 16 | Kein Artefakt-Typ „Policies" (ESRS-Pflicht) | Hoch | Offen |
| 17 | Kein Nachweis-/Prüfspur-Layer (Disclosure ↔ Beleg) | Hoch | Offen |
| 18 | Kein Audit-/Assurance-Feedback-Record (intern & extern) | Mittel | Offen |

---

### 1 — Keine Single Source of Truth
**Problem:** `initiative-index.yaml` spiegelt Infos aus Briefs/Plänen (Status, Verknüpfungen); Zahlen (z. B. ~430.000 tCO₂e) stehen in Geschäftskontext, Inventar *und* Roadmap.
**Warum prinzipiell:** Mehrfach gehaltene Wahrheit driftet garantiert; Vertrauen ins OS bricht.
**Fix-Richtung:** Daten leben einmal (Inventar/Katalog), Narrativ referenziert statt kopiert.
**Konkret entdeckter Drift (Beleg):** Das Inventar 2025 schreibt die Scope-2-Senkung „PPA Tranche 1 wirksam" zu (also bereits geliefert), während Roadmap, Brief und Plan PPA Tranche 1 als 2026-Meilenstein mit Status „Vertrag final 🔄" führen. Widersprüchliche Aussage über denselben Sachverhalt.

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

### 12 — Fehlender Jahresprogramm-/Planungs-Layer
**Problem:** Es gibt kein eigenständiges „Jahresprogramm 2026"-Artefakt. Die Frage „Was ist unser Programm dieses Jahr?" musste aus Roadmap-Zeile + Index-Status + Brief-Meilensteinen rekonstruiert werden.
**Warum prinzipiell:** Zwischen mehrjähriger Roadmap und einzelnen Initiativen fehlt der zeitlich gerahmte Operating-Layer (Jahres-/Quartalsziele, OKR-artig) — für Teams, die in solchen Zyklen planen, eine Kernsicht.
**Fix-Richtung:** Ein `programs/annual/2026-programm.md` (oder Planungs-Layer), das Initiativen + Zielwerte je Jahr bündelt und auf die Detailartefakte verweist.

### 13 — Stakeholder-Ansprechpersonen nicht strukturiert
**Problem:** Das Stakeholder-Register (`programs/stakeholders/CLAUDE.md`) listet Stakeholder, aber Ansprechpersonen stehen — wenn überhaupt — nur im Fließtext einzelner Account-Dokumente. Die Accounts sind zudem uneinheitlich befüllt (z. B. `lieferant-acme-stahl/` und `procurement/` ausgearbeitet, `finance-controlling/` nur als Platzhalter referenziert). Die Frage „Wer ist unsere Ansprechperson bei Finance?" ist daher aus dem OS **nicht** beantwortbar.
**Warum prinzipiell:** „Wer ist mein Kontakt bei X?" ist eine Kernfrage ans OS — und scheitert an fehlenden strukturierten Kontaktfeldern + lückenhafter Account-Abdeckung (Spezialfall von #2).
**Fix-Richtung:** `ansprechperson` als strukturiertes Feld im Stakeholder-Register; Mindest-Stub-Pflicht pro gelistetem Account.

### 14 — Kein Record durchgeführter Maßnahmen
**Problem:** Das OS trackt nur *vorausschauenden* Status (`in Umsetzung / geplant / Discovery`) und Meilenstein-Häkchen, aber keine durchgeführten Maßnahmen. Die Frage „Was wurde dieses Jahr umgesetzt?" ist nicht sauber beantwortbar: keine Initiative ist „abgeschlossen", ✅-Meilensteine haben uneinheitliche/fehlende Abschlussdaten, und es gibt kein Aktivitäts-/Done-Log.
**Warum prinzipiell:** „Was haben wir erreicht?" ist eine Kern-Reporting- und Steuerungsfrage (auch für ESRS E1-3 „Maßnahmen"). Ohne Done-Record bleibt sie an Erinnerung gebunden — genau das, was das OS auflösen soll.
**Fix-Richtung:** Maßnahmen-/Aktivitäts-Log mit Abschlussdatum (oder `abgeschlossen`-Status + `abgeschlossen_am` im Index); Meilensteine mit Pflicht-Datum.

### 15 — Wesentliche Themen außer E1 nicht operationalisiert
**Problem:** Die Wesentlichkeitsanalyse deklariert sechs wesentliche Themen (E1, E2, E5, S1, S2, G1), aber nur **E1 (Klima)** ist mit Daten, Metriken, Roadmap, Initiativen und Zielen hinterlegt. E2/E5/S1/S2/G1 existieren nur als Zeile im `esrs-datapoint-mapping.md` mit Status ⏳ — ohne Baseline, Metrik, Datenquelle (außer grobem Pointer), Initiative oder Ziel. Beispiel: Für E5 (Metallschrott/Kreislauf) lässt sich kein Ziel ableiten, weil keinerlei Ausgangsdaten existieren. Zudem ist die `carbon-data/`-Ebene **ausschließlich THG/Klima** — es gibt keinen Ort für nicht-klimatische Umwelt-/Sozial-Metriken.
**Warum prinzipiell:** Das OS verspricht über die Wesentlichkeit mehr, als es trägt — für 5 von 6 wesentlichen Themen kann es keine Frage beantworten. Die Datenarchitektur ist klima-zentriert statt an den deklarierten Themen ausgerichtet.
**Fix-Richtung:** Entweder Scope ehrlich auf Klima begrenzen, oder pro wesentlichem Thema mindestens Baseline-Metrik + Datenquelle + Owner anlegen; Datenebene über THG hinaus öffnen (z. B. `carbon-data/` → `sustainability-data/` mit Metrik-Bereichen je Thema).
**Weitere Belege (E2-Test):** E2 ist als wesentlich deklariert, fehlt aber **komplett im Datenpunkt-Mapping** (`reporting/esrs-datapoint-mapping.md` listet E2 nicht) → Drift zwischen Wesentlichkeit und Reporting. Zudem ist der Fachbegriff „Prozessemissionen" (Kern von E2) **im Glossar nicht definiert** — die Terminologie deckt nur Klima/THG ab.

### 16 — Kein Artefakt-Typ „Policies"
**Problem:** ESRS verlangt Offenlegung von Policies je wesentlichem Thema (E1-2, E2-1, S1-1 …). Das OS hat **keinen** Policies-Bereich; im E1-Mapping verweist E1-2 nur auf „(Policy-Dok, Stub)". Für E2 etc. existiert nichts.
**Warum prinzipiell:** Policies sind ein eigener, pflichtiger Offenlegungs- und Governance-Bestandteil — sie gehören als Artefakt-Typ ins OS, nicht als Fußnote.
**Fix-Richtung:** `policies/`-Bereich (je Thema), referenziert aus dem Datenpunkt-Mapping.

### 17 — Kein Nachweis-/Prüfspur-Layer
**Problem:** Disclosures sind nicht mit ihren **Belegen** verknüpft (Quelldokumente, Berechnungen, Freigaben). `reporting/assurance/` ist nur als leerer Stub erwähnt. Die Frage „Wo liegen die Nachweise für E2-Angaben?" ist nicht beantwortbar.
**Warum prinzipiell:** Limited Assurance basiert auf nachvollziehbaren Belegen je Angabe — ohne Evidence-Layer ist das OS nicht prüfsicher.
**Fix-Richtung:** Pro Datenpunkt ein Nachweis-Verweis (Beleg/Quelle/Freigabe) im Mapping; `reporting/assurance/`-Struktur mit Prüfspur.

### 18 — Kein Audit-/Assurance-Feedback-Record
**Problem:** Es gibt keine Historie von Prüf-Feedback (internes Audit, externe Assurance-Findings). „Welches Audit-Feedback gab es letztes Jahr?" ist nicht beantwortbar.
**Warum prinzipiell:** Audit-Findings und ihre Erledigung sind steuerungs- und prüfungsrelevant; ohne Record wiederholen sich Mängel.
**Fix-Richtung:** `reporting/assurance/findings/` (analog zu `data-quality-findings/`), datiert, mit Status/Erledigung.

---

## Nächste Schritte (nach Review)

1. Findings priorisieren (dk + Team).
2. Entscheiden: nur strukturelle Konventionen festziehen *oder* Ordnerstruktur überarbeiten.
3. Eine überarbeitete Template-Version ableiten.
