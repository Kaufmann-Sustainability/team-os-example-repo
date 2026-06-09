# Implementation

Die Umsetzungsebene — das Pendant zu „Engineering". Wo Briefs das „Was/Warum" festlegen, definieren Pläne das „Wie", und Datenqualitäts-Findings dokumentieren, wo Zahlen nicht stimmen (analog zu Bug-Investigations).

## Ordnerstruktur

```
implementation/
├── plans/                    # Umsetzungspläne für Reduktionsmaßnahmen & Datenprojekte
│   ├── scope-1-2/
│   ├── scope-3/
│   └── reporting/
└── data-quality-findings/    # Untersuchte Datenfehler/-lücken (analog Bug-Investigations)
    └── scope-3/
```

## Pläne

| Plan | Initiative | Status |
|------|-----------|--------|
| `plans/scope-1-2/renewable-electricity-ppa.md` | Grünstrom-PPA | In Umsetzung |
| `plans/scope-3/supplier-data-collection.md` | Lieferanten-Engagement | In Umsetzung |

## Datenqualitäts-Findings

Wenn das Inventar nicht plausibel ist (z. B. Sprung ohne realen Grund, Doppelzählung, Methodenbruch), wird ein Finding angelegt: **Symptom · Untersuchung · Ursache · Korrektur · Reporting-Auswirkung.**

| Finding | Bereich | Status |
|---------|---------|--------|
| `data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md` | Scope 3 Kat. 1 | Korrektur eingeplant |
