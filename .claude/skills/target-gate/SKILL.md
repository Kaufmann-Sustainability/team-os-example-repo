---
name: target-gate
description: Vollständigkeits-Wächter für Ziele (target-*). Einsetzen, wenn ein Target angelegt oder geändert wird — stellt sicher, dass das ganze Steuerungs-Gerüst (Owner, IRO-Bezug, KPI, Maßnahme, Annahme, Freigabe, Risiken) entweder befüllt ODER explizit als offener Punkt markiert ist. Kein Ziel kommt unvollständig und unmarkiert ins System.
---

# Skill: Target-Gate (Vollständigkeits-Vertrag für Ziele)

Ein Ziel ist erst dann *gesteuert*, wenn klar ist: wem es gehört, welche IRO es adressiert,
womit es gemessen wird, welche Maßnahmen es tragen, worauf es beruht, wer es freigegeben hat und
was seine Erreichung gefährdet. Dieser Skill ist der **Wächter**: Er lässt ein Ziel rein, aber
**nie still unvollständig** — jede Lücke ist entweder gefüllt oder als `offene_punkte` markiert.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Umsetzung |
|---|---------|-----------|
| 1 | **Verantwortung (RASCI)** | `owner: person-…` = **Accountable** (genau einer, muss existieren) · **≥1 `responsible: [person-…]`** (führt aus) · optional `consulted`/`informed`. **Accountable ≠ Responsible ist erlaubt** (formell verantwortlich vs. ausführend). Owner-Wechsel nur über ein `handover` (von/an/bestätigt) — **nie still**. |
| 2 | **Messbar** | `baseline_wert` + `zielwert` + `zieljahr` + `einheit` + `geltungsbereich` |
| 3 | **≥1 IRO** | `addresses: [iro-…]` — wofür existiert das Ziel? (→ `iro-coverage`) |
| 4 | **≥1 KPI** | `measured_by: [kpi-…]` — woran misst man Fortschritt? (→ `performance-tracking`) |
| 5 | **≥1 Maßnahme** | `supported_by: [initiative-…]` — wie wird es erreicht? (→ `measure-planning`) |
| 6 | **≥1 Annahme** | ein `assumption` mit `underpins: [dieses target]` (→ `assumption-register`) |
| 7 | **Freigabe** | ein `approval` mit `approves: [dieses target]` (Gremium + Datum + Genehmiger) |
| 8 | **Risiken bewertet** | ≥1 `risk` mit `threatens: [dieses target]` — **oder** bewusst „keine wesentlichen" als offener Punkt |
| + | *Bonus* | `scenario` (Was-wäre-wenn), Evidenz auf KPI-Ebene |

> **Risk ≠ IRO.** Ein Zielerreichungs-Risiko (Förderwegfall, Fachkräftemangel) ist ein eigenes
> `risk`-Objekt, **keine** DMA-Wesentlichkeits-IRO. Verwechsle die beiden nicht.

## Ablauf
1. **Vertrag prüfen:** `python3 tools/query.py reifegrad <target-id>` (oder `<topic-id>` für alle Ziele).
2. **Lücken schließen** — fehlendes Objekt anlegen (Annahme, Approval, Risk …) und verlinken.
3. **Was (noch) nicht geht, markieren:** unerledigte Punkte als `offene_punkte:`-Liste ins
   Front-Matter des Targets — so ist die Lücke sichtbar, nicht verschwunden.
4. **Erneut prüfen** bis Reifegrad 100 % **oder** jede Restlücke ein bewusster `offene_punkt` ist.

## Harte Regeln
- 🚫 **Kein Ziel ohne Owner, IRO-Bezug, KPI und Maßnahme** — das ist das nicht verhandelbare Minimum.
- 🚫 **Keine stille Lücke.** Punkt 6–8 fehlen? → anlegen *oder* `offene_punkte` eintragen. Nie einfach weglassen.
- ✅ **Freigabe ist eine eigene Spur.** Status `in-umsetzung` ohne `approval` ist ein Widerspruch → markieren.
- 🔗 **Risiken verlinken statt beschreiben.** Ein Risiko im Fließtext zählt nicht; es braucht ein `risk`-Objekt mit `threatens`.

## Vor dem Abschluss
- [ ] `reifegrad <target>` zeigt 100 % **oder** jede offene Pflicht steht in `offene_punkte`
- [ ] Approval-Genehmiger ≠ Owner (Funktionstrennung), wo es um echte Freigaben geht
- [ ] `validate.py` grün

> Dieser Skill ist die **Vorlage** für die übrigen Objekt-Gates (topic/iro/kpi/initiative):
> gleicher Aufbau — Vertrag, `reifegrad`-Check, `offene_punkte`-Marker.
