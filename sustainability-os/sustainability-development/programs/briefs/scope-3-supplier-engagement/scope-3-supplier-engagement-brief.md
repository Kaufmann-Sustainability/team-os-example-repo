# Initiativen-Brief: Scope-3 Lieferanten-Engagement

**Owner:** Jonas Fischer (Supplier Sustainability Lead) · **Sponsor:** Dr. Lena Hartmann · **Säule:** Scope 3 · **Status:** In Umsetzung · **Tickets:** SUS/231, SUS/240, SUS/245

## Problem / Anlass

~79 % von Nordmarks Emissionen liegen in Scope 3, davon der Löwenanteil in Kategorie 1 (eingekaufte Güter — v. a. Stahl und Aluminium). Heute wird Kat. 1 **spend-based** geschätzt (Ausgaben × generischer Emissionsfaktor). Das ist:
- **ungenau** — bildet keine Lieferanten-spezifischen Reduktionsanstrengungen ab,
- **nicht steuerbar** — wir sehen nicht, welcher Lieferant welchen Fußabdruck hat,
- **reporting-riskant** — Wirtschaftsprüfer hinterfragen spend-based-Daten zunehmend.

## Ziel & Erfolgsmetrik

| Ziel | Metrik | Zielwert | Frist |
|------|--------|----------|-------|
| Primärdaten-Abdeckung erhöhen | % Kat.-1-Emissionen mit lieferanten-spezifischen EFs | ≥ 60 % | Ende 2027 |
| Lieferanten zu Zielen bewegen | % Top-20-Lieferanten mit eigenem SBTi-Commitment | ≥ 50 % | Ende 2028 |
| Scope-3-Reduktion | Intensität kgCO₂e/t Produkt | −25 % vs. 2024 | 2030 |

## Scope

**In Scope:** Top-20-Lieferanten nach Emissionsbeitrag (decken ~75 % der Kat.-1-Emissionen ab), Stahl- und Alu-Lieferanten priorisiert.
**Out of Scope:** Tail-Spend-Lieferanten (bleiben vorerst spend-based), Scope-3-Kategorien 11/12 (eigene Initiative).

## Reduktionshebel

1. **Datenerhebung:** Lieferanten-Fragebogen + Anbindung an CDP/Branchenplattform → lieferanten-spezifische EFs ersetzen generische.
2. **Engagement:** Lieferanten-Scorecard, jährliches Nachhaltigkeits-Review im Einkaufsgespräch, CO₂ als Vergabekriterium.
3. **Material-Shift:** Wechsel auf grünen Stahl (H2-/Schrott-Route) bei bereiten Lieferanten.

## Abhängigkeiten

- **Procurement** (`../../stakeholders/accounts/procurement/`) — muss CO₂ ins Vergabe-Scoring aufnehmen.
- **Carbon Data** — Aufnahme lieferanten-spezifischer EFs als `ef-*`-Objekte (`../../../../object-model/objects/`).
- **Datenqualität** — bekanntes Doppelzählungs-Risiko beim Übergang spend→supplier (siehe `../../../implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md`).

## Reporting-Bezug (ESRS)

- **E1-6** Brutto-THG Scope 3 — Verbesserung der Datenqualität ist offenlegungspflichtig (Methodik & Anteil Primärdaten).
- **G1** Lieferanten-Beziehungen — Engagement-Praktiken.

## Meilensteine

| Meilenstein | Frist | Status |
|-------------|-------|--------|
| Top-20 nach Emissionsbeitrag identifiziert | Q1 2026 | ✅ |
| Lieferanten-Fragebogen ausgerollt | Q2 2026 | 🔄 |
| Erste 5 lieferanten-spezifische EFs im Katalog | Q4 2026 | ⏳ |
| 60 % Primärdaten-Abdeckung | Q4 2027 | ⏳ |

## Umsetzungsplan

Detail-Plan: `../../../implementation/plans/scope-3/supplier-data-collection.md`
