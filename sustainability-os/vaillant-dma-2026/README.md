# Vaillant DMA 2026 — importierter Objektgraph

> **Was das ist:** Eine **echte Doppelte Wesentlichkeitsanalyse** (Vaillant, 2026),
> automatisiert aus dem DMA-Skill-Output (Excel) ins Objektmodell überführt.
> Bewusst **getrennt** vom fiktiven Nordmark-Beispiel (`../object-model/`), damit reale
> und Demo-Daten nicht vermischen.

## Inhalt
- **170 IROs** (`iro-*`) — 120 wesentlich + 50 nicht-wesentlich (Letztere als Ausschluss-Begründung, prüfungsrelevant).
- **89 Themen** (`topic-*`) — je ESRS-Standard + Sub-Thema; 71 wesentlich, 18 nicht-wesentlich (`status`).
- **34 Dependencies** (`dependency-*`) — Abhängigkeiten von natürl./sozialem Kapital je Standard (DMA Sheet 2), mit R/O-Relevanz.
- **1 `decision-dma-2026`** — append-only Jahres-Record (`affects` → alle 89 Themen).
- **1 `methodology-dma-2026`**, **1 `person-dma-lead`** (Platzhalter-Owner).

**608 Objekte, Validator grün** (inkl. der voll gesteuerten Themen + templatisierter Rest).

## Vollmodelliertes Beispiel: E1 Klimawandel-Mitigation
Ein Bereich exemplarisch von *bewertet* zu *gesteuert* gebracht (statt Template):
- **1 Strategie** + **2 Policies** + **5 Ziele** + **6 KPIs** + **6 Maßnahmen** (echte Rollen-Owner,
  Budgets, verlinkte Dependencies) + **1 Grundsatz-Entscheidung**.
- Neue Kanten: **`addresses`** (Ziel/Strategie/Policy → IRO, *many-to-many* — das Kernziel
  „Wärmepumpen-Absatzanteil" deckt 8 IROs ab) und **`depends_on`** (Maßnahme → Dependency).
- Konsistenz prüfbar: `python3 tools/query.py coverage topic-e1-klimawandel-mitigation`
  (jede wesentliche IRO abgedeckt; ◐ = nur Strategie/Policy, kein Metrik-Ziel).
- **Emergente Skills** (global, `.claude/skills/`): `iro-coverage` (IRO-Abdeckung) und
  `measure-planning` (Maßnahme = Owner+Budget+Dependencies) — wahren die Konsistenz wie der
  `sustainability-standard`-Skill die Baseline.

## So wurde es erzeugt (reproduzierbar)
```bash
python3 tools/import_dma.py <pfad-zur-DMA.xlsx>   # Excel -> Objekte
python3 tools/validate.py                          # Integrität (referenzielle Kanten, Pflichtfelder)
python3 tools/query.py stats                        # Übersicht
```
Der Importer (`tools/import_dma.py`) liest das Blatt **IRO-Liste**, filtert auf wesentliche
IROs, gruppiert sie nach **Standard + Sub-Thema** zu Themen und mappt:
`Impact-/Financial-Score → impact_/finanz_wesentlichkeit` (4-5 hoch · 3 mittel · 1-2 niedrig),
`Typ (I-/I+/R/O) → iro_typ`, `Material? → wesentlich`, Beschreibung+Begründung → Body.

## Das ist der Beweis
Der Schritt *„DMA-Skill-Output → kanonisches Objektmodell"* ist **automatisierbar und
prüfbar**, nicht handgeklöppelt: Ein reales 170-Zeilen-DMA (davon 120 wesentlich) landet
deterministisch als Objektgraph — append-only, mit referenzieller Integrität, abfragbar.

## Konventionen
- **ID-Stabilität:** `iro-<IRO-Nr>` und `topic-<standard>-<sub-thema>` — ein erneuter Import
  desselben Jahres aktualisiert dieselben Objekte (kein Duplikat).
- **Append-only:** Ein neues DMA-Jahr legt `decision-dma-<jahr>` zusätzlich an; die
  Git-Historie ist die Versionierung der Bewertung (Score-Änderungen je `git diff`).
- Schema: `object-schema.yaml` (Kopie der Nordmark-Konvention).
