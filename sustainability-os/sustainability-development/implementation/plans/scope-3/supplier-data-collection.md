# Umsetzungsplan: Lieferanten-Datenerhebung (Scope 3)

**Brief:** `../../../programs/briefs/scope-3-supplier-engagement/scope-3-supplier-engagement-brief.md` · **Owner:** Jonas Fischer · **Beteiligt:** Tobias Klein (Carbon Data), Procurement · **Tickets:** SUS/240, SUS/245

## Ziel des Plans

Lieferanten-spezifische Primärdaten von den Top-20-Lieferanten erheben und als `ef-*`-Objekte (unter `../../../object-model/objects/`) überführen, sodass Scope-3-Kat.-1 von spend-based auf supplier-specific umgestellt werden kann.

## Arbeitspakete

| # | Paket | Owner | Status |
|---|-------|-------|--------|
| 1 | Top-20-Lieferanten nach Emissionsbeitrag priorisieren | Tobias | ✅ |
| 2 | Fragebogen (EF, Methodik, Reduktionsziele) entwerfen | Jonas | ✅ |
| 3 | Versand & Nachverfolgung (CDP / interne Plattform) | Jonas | 🔄 |
| 4 | Rücklauf-Validierung & Plausibilisierung | Tobias | ⏳ |
| 5 | EFs als `ef-*`-Objekte überführen (`ef-stahl-supplier-specific.md` etc.) | Tobias | ⏳ |
| 6 | Umstellung Inventar-Berechnung + Neuberechnung Basisjahr | Sophie | ⏳ |

## Wichtige Designentscheidung

Beim Wechsel spend→supplier muss sichergestellt sein, dass **kein Volumen doppelt gezählt** wird (einige Spend-Positionen enthalten bereits weiterverarbeitete Vormaterialien). Siehe Finding `../../data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md` — die Korrektur ist in Paket 6 eingeplant.

## Datenfluss

ERP-Spend + Lieferanten-Fragebogen → Validierung → `ef-*`-Objekte unter `../../../object-model/objects/` → `carbon-data/inventory/` → Reporting (ESRS E1-6).
