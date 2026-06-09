---
name: iro-coverage
description: Sicherstellen, dass jede WESENTLICHE IRO eines Themas durch Strategie, Policy und/oder Ziele abgedeckt ist (many-to-many — ein Ziel kann mehrere IROs abdecken). Einsetzen, wenn ein Thema von „bewertet" (IROs aus der DMA) zu „gesteuert" gebracht wird, oder wenn sich IROs/Ziele ändern — damit keine wesentliche IRO unadressiert bleibt und kein Ziel ohne IRO-Bezug existiert.
---

# Skill: IRO-Abdeckung (Themen-Steuerung)

Dieser Skill bringt ein Thema von **bewertet → gesteuert**. Ausgangslage: ein Topic mit seinen
IROs (aus der DMA). Ergebnis: Strategie + Policies + Ziele, die **gemeinsam jede wesentliche IRO
abdecken** — über die `addresses`-Kante (`target/strategy/policy → addresses → iro`). Ein Ziel
darf (und soll oft) **mehrere IROs** abdecken; mehrere Ziele dürfen sich eine IRO teilen.

> Komponiert mit `sustainability-standard` (Baseline-Disziplin je Ziel) und `measure-planning`
> (Maßnahmen mit Owner/Budget/Dependencies).

## Ablauf
1. **IROs sichten.** Lies `topic-*.md → has_iro`; filtere die **wesentlichen** (`wesentlich: ja`).
   Gruppiere sie nach Management-Logik (z. B. „Use-Phase", „eigene Emissionen", „Vorkette",
   „Finanzrisiken/Chancen").
2. **Strategie & Policy festlegen.** Eine `strategy` (Transitionsplan) + ≥1 `policy` je Thema;
   beide verweisen über `addresses` auf die IROs, die sie steuern (besonders Risiken/Chancen,
   die *strategisch* statt über ein Metrik-Ziel gemanagt werden).
3. **Ziele setzen — IRO-getrieben.** Pro Cluster ein `target` mit `addresses: [iro, …]`. Ein
   starkes Ziel deckt Risiken **und** Chancen **und** positive Impacts zugleich ab (Beispiel:
   „Wärmepumpen-Absatzanteil" deckt Stranding-Risiko, Marktchance und positiven Use-Phase-Impact).
4. **Prüfen.** `python3 tools/query.py coverage <topic-id>` ausführen.

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Keine wesentliche IRO ohne Abdeckung.** Jede `wesentlich: ja`-IRO muss von ≥1
  `target` **oder** (bewusst) von Strategie/Policy adressiert sein. Sonst: Lücke schließen.
- ⚠ **„Nur Strategie/Policy, kein Metrik-Ziel" ist erlaubt, aber bewusst.** Typisch für reine
  Finanz-/Reputationsrisiken. Der `coverage`-Check markiert das mit `◐` — bestätigen, nicht ignorieren.
- 🚫 **Kein Orphan-Ziel.** Jedes `target` muss ≥1 IRO über `addresses` adressieren — sonst: warum
  existiert es?
- 🔗 **Jedes Ziel braucht ≥1 KPI (`measured_by`) und ≥1 Maßnahme (`supported_by`).**
- 🧭 Baseline/Einheit/Zieljahr je Ziel nach `sustainability-standard`.

## Vor dem Abschluss
- [ ] `query.py coverage <topic>` → „Jede wesentliche IRO ist adressiert."
- [ ] Alle `◐`-Fälle (nur Strategie/Policy) bewusst bestätigt
- [ ] Kein Orphan-Ziel; jedes Ziel mit KPI + Maßnahme
- [ ] `validate.py` grün
