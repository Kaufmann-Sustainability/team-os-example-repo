---
id: decision-e1-iro-kpi-zuordnung
type: decision
owner: person-dma-lead
status: beschlossen
stand: 2026-06-11
review_zyklus: P12M
vertraulichkeit: intern
esrs_bezug: E1
datum: 2026-06-11
entscheidung: "Jede wesentliche E1-IRO wird einer oder mehreren bestehenden Klima-KPIs zugeordnet (Kante iro→measured_by→kpi), damit der ESRS-Anspruch ‚jede wesentliche IRO ist messbar' erfüllt ist — unabhängig davon, ob ein Metrik-Ziel existiert."
begruendung: "ESRS verlangt, dass wesentliche IROs durch Kennzahlen abgebildet werden; die Steuerung über Ziele/Policies ist demgegenüber frei. Die Zuordnung folgt der Management-Logik der bestehenden Ziele: Nutzungsphasen-Impacts (I5/I6) und die Markt-Risiken/Chancen (R1/R2/R4/O1–O3) auf den Wärmepumpen-Absatzanteil und die vermiedenen Emissionen; eigene Emissionen (I2) auf Scope-1-2; Vorkette (I3) auf Scope-3.1-Intensität; Logistik (I4) auf die Logistik-KPI. R3 (physisches/Übergangs-Restrisiko) bleibt bewusst ohne eigene Metrik und wird über die Transitionsstrategie gesteuert — als offener Punkt am Thema vermerkt."
decided_by: [person-dma-lead]
affects: [iro-e1-i1, iro-e1-i2, iro-e1-i3, iro-e1-i4, iro-e1-i5, iro-e1-i6, iro-e1-r1, iro-e1-r2, iro-e1-r4, iro-e1-o1, iro-e1-o2, iro-e1-o3, kpi-e1-waermepumpen-absatzanteil, kpi-e1-scope3-11, kpi-e1-vermiedene-emissionen, kpi-e1-scope1-2, kpi-e1-scope3-1-intensitaet, kpi-e1-logistik]
based_on: [methodology-dma-2026]
---

# Entscheidung: IRO→KPI-Zuordnung für E1 (Klimawandel-Mitigation)

ADR-Record der Mess-Verankerung. Erfüllt die ESRS-Pflicht, dass jede wesentliche IRO durch
≥1 Kennzahl abgebildet ist — die **Messung** (`iro → measured_by → kpi`) ist verbindlich, die
**Steuerung** (`addresses` durch Ziel/Policy/Strategie) bleibt optional.

| IRO-Cluster | IROs | KPI(s) |
|-------------|------|--------|
| Nutzungsphase (Impacts) | I1, I5, I6 | Scope-3.11, vermiedene Emissionen, Wärmepumpen-Absatzanteil |
| Markt-Risiken & -Chancen | R1, R2, R4, O1, O2, O3 | Wärmepumpen-Absatzanteil |
| Eigene Emissionen | I2 | Scope-1-2 |
| Vorkette (embodied) | I3 | Scope-3.1-Intensität |
| Logistik | I4 | Logistik-Index |
| Physisches/Übergangs-Restrisiko | R3 | — bewusst keine Metrik, Steuerung über Transitionsstrategie |

> **Educated Guess** — kein Vaillant-Originaldokument.
