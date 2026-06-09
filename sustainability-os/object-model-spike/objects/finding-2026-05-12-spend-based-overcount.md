---
id: finding-2026-05-12-spend-based-overcount
type: finding
owner: person-tobiasklein
status: offen
stand: 2026-06-09
review_zyklus: P1M
vertraulichkeit: intern
esrs_bezug: E1-6
datum: 2026-05-12
quelle: sustainability-development/implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md
# Beziehungen
affects: [kpi-scope3-intensitaet, target-sbti-scope3-2030]
---

# Finding: Doppelzählung spend-based Scope-3 Kat. 1

Graph-natives Spiegel-Objekt des bestehenden Datenqualitäts-Findings
(`../../sustainability-development/implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md`).
Der volle Untersuchungstext lebt dort; hier zählen die **Kanten und der Status**.

## Kern
Spend-based-Faktor zählt Vormaterialien doppelt → Kat.-1-Emissionen ~12 % zu hoch →
**Baseline 2024 muss neu berechnet werden.** Status: **offen** (Korrektur im Umsetzungsplan).

## Warum dieses Objekt der Beweis des Spikes ist
Es `affects` sowohl den KPI als auch das Target. Ein naiver Target-Setting-Kontext
(„Berechnungsdetails ausschließen") würde genau dieses Faktum verbergen — und damit ein
Ziel auf einer falschen Baseline setzen. Die **Eskalations-Klausel** des Packs zieht jede
offene Finding, die Baseline/Metrik berührt, **immer** mit hinein. So wird aus „minimal"
nicht „lückenhaft".
