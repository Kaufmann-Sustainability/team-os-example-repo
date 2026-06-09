---
name: assurance
description: Prüfspur für offenlegungsrelevante Kennzahlen aufbauen — Control, Test, Evidence, Finding, Remediation. Einsetzen, wenn ein KPI/Datenpunkt prüfsicher werden soll, damit jede berichtsrelevante Kennzahl eine getestete Kontrolle und jedes offene Finding eine Remediation hat („können wir es beweisen?").
---

# Skill: Assurance (Prüfspur)

Macht eine Kennzahl **prüfsicher**: eine Kontrolle sichert sie ab, ein Test belegt deren
Wirksamkeit, Evidenz stützt die Werte, Findings + Remediations schließen Schwächen.

## Die Kette
```
kpi / target  ──covers──  control  ──tests──  test
kpi-value     ──backs──   evidence
finding  ──affects──  kpi        finding  ──remediates──  remediation
```

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Keine offenlegungsrelevante KPI ohne Kontrolle.** Jede berichtsrelevante `kpi` (bzw.
  `target`) braucht ≥1 `control` (`covers`).
- 🧪 **Keine Kontrolle ohne Test.** Jede `control` braucht ≥1 `test` (`tests`) — ungetestete
  Kontrolle ist nur eine Behauptung.
- 📎 **Werte brauchen Evidenz.** Reporting-relevante `kpi-value` über `evidence` (`backs`) belegen.
- 🚫 **Kein offenes Finding ohne Remediation.** Jedes `finding`/`audit-finding` mit `status: offen`
  braucht eine `remediation` (`remediates`). (Beispiel: `finding-e1-usephase-annahmen` →
  `remediation-e1-usephase`.)
- ⛔ **Gate:** Solange ein offenes Finding einen berichteten KPI berührt, ist der zugehörige
  Wert *vorläufig* — keine finale Offenlegung (vgl. `disclosure`-Pack-Gate).

## Vor dem Abschluss
- [ ] Jede berichtsrelevante KPI: Kontrolle + Test + (Werte mit) Evidenz
- [ ] Jedes offene Finding: Remediation verlinkt
- [ ] `validate.py` grün
