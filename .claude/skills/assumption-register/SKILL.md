---
name: assumption-register
description: Annahmen hinter Zielen, Entscheidungen und Szenarien explizit machen — mit Confidence und Quelle. Einsetzen, wenn ein Ziel/eine Entscheidung gesetzt wird, die auf Annahmen beruht, damit „worauf beruht das?" abfragbar wird und Ziele auf wackligen (niedrig-Confidence-)Annahmen sichtbar bleiben.
---

# Skill: Annahmen-Register

Macht **Provenienz** erstklassig: Jede tragende Annahme wird ein `assumption`-Objekt mit
`confidence` (hoch/mittel/niedrig) und `quelle`, verlinkt über `underpins` auf das Ziel / die
Entscheidung / das Szenario, das darauf ruht. So ist „worauf beruht das?" eine Ein-Hop-Abfrage —
nicht im Prosa-Body vergraben.

## Pflichtfelder je `assumption`
| Feld/Kante | Regel |
|------------|-------|
| `confidence` | **Pflicht** — hoch / mittel / niedrig |
| `quelle` | Woher die Annahme stammt (Team, Studie, Marktdaten) |
| `underpins` | ≥1 `target`/`decision`/`scenario`, das auf der Annahme ruht |

## Harte Regeln (Konsistenz erzwingen)
- 🚫 **Keine Annahme ohne Confidence + Quelle.**
- ⚠ **Niedrig-Confidence-Annahme unter einem Ziel → markieren.** Sie ist ein Risiko-Signal;
  prüfe, ob ein Risiko-IRO existiert (oft ja) und ob eine `recommendation` (Hedge) sinnvoll ist.
  (Beispiel: `assumption-e1-foerderung` (niedrig) ↔ Risiko `iro-e1-r4` ↔ `recommendation-e1-foerder-hedge`.)
- 🧪 **Szenarien deklarieren ihre Annahmen** über `assumes` — ein Szenario ohne Annahmen ist Spekulation.
- 🔄 Annahmen sind **append-/versionierbar**: ändert sich die Confidence (z. B. nach neuer Evidenz),
  `stand` hochsetzen; Git ist die Historie.

## Vor dem Abschluss
- [ ] Jede tragende Annahme: `confidence` + `quelle` + `underpins`
- [ ] Niedrig-Confidence-Annahmen unter Zielen bewusst (Risiko-IRO / Empfehlung geprüft)
- [ ] `validate.py` grün
