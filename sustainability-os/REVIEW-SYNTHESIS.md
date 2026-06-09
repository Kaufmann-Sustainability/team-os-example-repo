# Review-Synthese & Ziel-Struktur

> **Update 2026-06-09:** Das OS wurde inzwischen vollständig auf das Objektmodell (`object-model/`) umgestellt; die hier erwähnten Registries (`targets.yaml`, `glossary.md`, `initiative-index.yaml`, EF-Katalog) sind in Objekte migriert und gelöscht.

> Verdichtet die 19 Findings aus [`REVIEW-FINDINGS.md`](REVIEW-FINDINGS.md) auf **5 Grundprobleme** und entwirft die überarbeitete OS-Struktur, die sie adressiert. **Stand:** 2026-06-09 · **Status:** Entwurf zur Freigabe (noch nicht umgesetzt).

---

## Teil 1 — Die 5 Grundprobleme

### A — Fakten liegen in Prosa, nicht strukturiert; keine Single Source of Truth
*(Findings #1, #2, #11, #13)*
Owner, Status, Kontakt, Zahlen, Definitionen und Ziele stehen im Fließtext — oft mehrfach kopiert, ohne kanonische Quelle. Folge: Strukturierte Fragen („Wer ist verantwortlich?", „Was ist der Status?") sind unzuverlässig beantwortbar, und kopierte Fakten driften auseinander (belegt durch den PPA-Widerspruch).
**Kern:** Strukturierte Fakten + genau eine kanonische Quelle je Fakt.

### B — Das OS ist ein Klima-OS, kein Nachhaltigkeits-OS; Taxonomie ist branchengebunden
*(Findings #5, #15)*
Sechs wesentliche Themen sind deklariert, aber nur E1 (Klima) ist mit Daten, Metriken, Zielen und Initiativen unterlegt. E2/E5/S1/S2/G1 sind hohl. Die oberste Gliederung (Scope 1&2 / Scope 3 / Reporting) unterstellt zudem einen Hersteller.
**Kern:** Vollständige Abdeckung *aller* wesentlichen Themen + eine generische, CSRD-native Gliederung.

### C — Wesentliche Artefakt-Typen & Lebenszyklus-Layer fehlen
*(Findings #3, #4, #12, #14, #16, #17, #18, #19)*
Das OS kennt Pläne (Briefs) und Probleme (Findings) — aber nicht: Entscheidungen mit Begründung, Policies, einen Jahresplanungs-Layer, durchgeführte Maßnahmen (Done-Log), Nachweise/Prüfspur, Audit-Feedback und den versionierten Berichtstext. Gerade die offenlegungs- und prüfungsrelevanten Schichten fehlen.
**Kern:** Den vollständigen Lebenszyklus abbilden — von der Entscheidung bis zum geprüften Bericht.

### D — Keine Inhalts-Governance: Aktualität, Versionierung, Vertraulichkeit, Systemgrenze
*(Findings #6, #7, #8, #9)*
Man sieht Dokumenten ihr Alter nicht an, Restatements/Versionen sind nicht modelliert, Vertrauliches ist nicht markiert, und die Grenze „Was lebt im OS vs. im System of Record (SAP/Power BI)?" ist undefiniert.
**Kern:** Jedes Artefakt trägt Lebenszyklus-Metadaten; klare Regeln für Daten-Versionierung, Sensitivität und Systemgrenze.

### E — Keine maschinelle Konsistenz-/Integritätssicherung
*(Finding #10, plus der Durchsetzungs-Aspekt von #1)*
Querverweise und Index sind handgepflegt; nichts erkennt Drift, tote Links oder unvollständige Einträge. Der einzige „Wächter" ist Aufmerksamkeit.
**Kern:** Automatisierte Checks, die Konsistenz erzwingen statt erhoffen.

---

## Teil 2 — Leitprinzipien der Ziel-Struktur

1. **Registries vor Prosa.** Cross-cutting-Fakten (Initiativen, Ziele, Metriken, Stakeholder, Begriffe) leben *einmal* in strukturierten Registries; Dokumente verweisen, statt zu kopieren. *(A)*
2. **Metadaten-Kopf auf jedem Artefakt.** Pflicht-Front-Matter: `owner, status, stand, review_zyklus, vertraulichkeit, esrs_bezug, quelle`. *(A, D)*
3. **Gliederung nach wesentlichem Thema** (E1/E2/E5/S1/S2/G1) statt nach Scope. CSRD-native, industrie-agnostisch, und macht Lücken sichtbar (leerer E2-Ordner = sichtbare Aufgabe). Scope 1/2/3 wird zur *Unterstruktur innerhalb E1*. *(B)*
4. **Jeder Artefakt-Typ existiert explizit.** Entscheidungen, Policies, Pläne, Maßnahmen-Log, Nachweise, Audit-Findings, Berichtstext — jeweils ein klar benannter Ort. *(C)*
5. **Daten getrennt von Narrativ; Daten versioniert.** Zahlen leben in der Datenebene (mit Jahres-/Restatement-Versionierung), Narrativ referenziert sie. *(A, D)*
6. **Konventionen sind dokumentiert und automatisiert geprüft.** Eine `CONVENTIONS.md` + CI-Checks. *(D, E)*

---

## Teil 3 — Überarbeitete Ziel-Struktur

```
sustainability-os/
├── CLAUDE.md · README.md · TOUR.md · MAINTAINING.md
├── CONVENTIONS.md              # NEU: Metadaten-Schema, Naming, OS↔System-Grenze, Sensitivität (D,#9)
├── REVIEW-FINDINGS.md · REVIEW-SYNTHESIS.md
└── sustainability-development/
    ├── CLAUDE.md
    ├── registries/             # NEU: Single Source of Truth, strukturiert (A)
    │   ├── initiatives.yaml     #   war initiative-index; owner/status/datum als Felder (#1,#2)
    │   ├── targets.yaml         #   ✓ existiert bereits
    │   ├── glossary.md          #   ✓ existiert bereits
    │   ├── metrics.yaml         #   NEU: KPI-Defs aller Themen, nicht nur Carbon (#15)
    │   └── stakeholders.yaml    #   NEU: inkl. strukturiertem Kontaktfeld (#13)
    ├── strategy/
    │   ├── sustainability-strategy.md   # NEU: kanonisches Strategie-Artefakt (#11)
    │   ├── materiality/                 # + Begründung je Thema (#3)
    │   └── roadmaps/
    ├── programs/               # gegliedert nach wesentlichem THEMA (B)
    │   ├── e1-klima/           #   briefs/ · plans/ · policies/   (Scope 1/2/3 hier drunter)
    │   ├── e2-umwelt/          #   bisher hohl → jetzt sichtbarer Platz (#15,#16)
    │   ├── e5-ressourcen/
    │   ├── s1-belegschaft/
    │   ├── s2-wertschoepfungskette/
    │   ├── g1-governance/
    │   └── annual/2026-programm.md      # NEU: Jahres-Planungs-Layer (#12)
    ├── data/                   # war carbon-data → thematisch geöffnet (B,#15)
    │   ├── inventory/          #   + Versionierungs-/Restatement-Konvention (#8)
    │   ├── emission-factors-catalog.yaml
    │   └── <topic>-metrics/    #   z. B. e5-kreislauf-metriken
    ├── decisions/              # NEU: ADR-Stil, trägt Begründung (#4,#3)
    ├── implementation/
    │   ├── plans/
    │   ├── activity-log/       # NEU: durchgeführte Maßnahmen, datiert (#14)
    │   └── data-quality-findings/       # ✓ existiert
    └── reporting/
        ├── esrs-datapoint-mapping.md    # + Nachweis-Verweis je Datenpunkt (#17)
        ├── disclosures/2026/            # NEU: versionierter Berichtstext je Datenpunkt (#19)
        └── assurance/
            ├── evidence/                # NEU: Prüfspur/Belege (#17)
            └── findings/                # NEU: Audit-Feedback, datiert (#18)
```

### Was sich konkret ändert (alt → neu)

| Alt | Neu | Grund |
|-----|-----|-------|
| `initiative-index.yaml` | `registries/initiatives.yaml` (owner/status als Felder) | A (#1,#2) |
| Terminologie in `CLAUDE.md` | kanonisch in `registries/glossary.md` | A (#1) |
| Ziele verstreut (Kontext, Roadmap) | `registries/targets.yaml` | A (#11) |
| `programs/strategy/...` als Ordner | + `sustainability-strategy.md` als Artefakt | A (#11) |
| Säulen Scope1&2 / Scope3 / Reporting | `programs/<thema>/` | B (#5,#15) |
| `carbon-data/` | `data/` (alle Themen) | B (#15) |
| — | `decisions/`, `policies/`, `annual/`, `activity-log/`, `disclosures/`, `assurance/` | C |
| — | `CONVENTIONS.md` + Metadaten-Kopf überall | D |
| — | CI: Link-Check, Index-Schema-Check, Drift-Check | E (#10) |

---

## Teil 4 — Grundproblem → Strukturänderung (Nachverfolgung)

| Grundproblem | Adressiert durch |
|--------------|------------------|
| A Strukturierte Fakten / SSoT | `registries/`, Metadaten-Kopf |
| B Themen-Vollständigkeit / Taxonomie | `programs/<thema>/`, `data/`, `metrics.yaml` |
| C Artefakt-Typen / Lebenszyklus | `decisions/`, `policies/`, `annual/`, `activity-log/`, `disclosures/`, `assurance/` |
| D Inhalts-Governance | `CONVENTIONS.md`, Metadaten-Kopf, Daten-Versionierung, `vertraulichkeit` |
| E Konsistenz-Automatisierung | CI-Checks; der `sustainability-standard`-Skill als „menschliche" Variante davon |

---

## Teil 5 — Migrationsplan (vorgeschlagen, phasenweise)

Nicht alles auf einmal. Reihenfolge nach Hebel/Risiko:

1. **Fundament (geringes Risiko, hoher Hebel):** `CONVENTIONS.md` + Metadaten-Schema festlegen; `registries/` einführen (Initiatives/Metrics/Stakeholders), bestehende Inhalte hineinziehen. → löst A.
2. **Taxonomie-Umbau:** `programs/` und `data/` auf Themen umstellen. → löst B. *(Größter Eingriff — eigene Entscheidung, siehe unten.)*
3. **Fehlende Layer ergänzen:** `decisions/`, `policies/`, `annual/`, `activity-log/`, `reporting/disclosures|assurance/`. → löst C.
4. **Governance schärfen:** Daten-Versionierung, Sensitivitäts-Markierung. → löst D.
5. **Automatisierung:** CI-Checks (Links, Schema, Drift) + optional SessionStart-Hook. → löst E.

### Offene Entscheidung (blockiert Phase 2)

Der **Taxonomie-Umbau (Gliederung nach Thema statt Scope)** ist der größte und am schwersten umkehrbare Schritt — und er hängt am noch offenen Zielbild (konkretes In-house-OS vs. wiederverwendbares Template). Themen-Gliederung ist für ein *Template* klar besser (generisch); für ein *einzelnes Hersteller-Team* wäre die Scope-Gliederung evtl. vertrauter. Diese Entscheidung sollte vor Phase 2 fallen.
