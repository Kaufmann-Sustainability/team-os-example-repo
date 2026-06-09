---
name: sustainability-standard
description: Standardisierte Definitionen und Ziele für das Sustainability OS formulieren. Einsetzen, wenn jemand (auch aus HR, Procurement oder anderen Fachbereichen) einen Nachhaltigkeits-Begriff bzw. eine Kennzahl definieren oder ein Ziel/Target festlegen will — damit das Ergebnis den OS-Konventionen folgt, vollständig ist und konsistent zu bestehenden Einträgen bleibt.
---

# Skill: Standardisierte Definition oder Ziel

Dieser Skill macht es **jedem Teammitglied — auch ohne Nachhaltigkeits-Fachhintergrund** — möglich, einen Begriff zu definieren oder ein Ziel festzulegen, das sich sauber ins Sustainability OS einfügt. Das Nachhaltigkeitsteam legt die *Konvention* einmal fest (hier); HR, Procurement & Co. bedienen sie selbst. Ergebnis: konsistente, vollständige, prüfsichere Einträge statt verstreuter Definitionen in Köpfen und Mails.

## Zwei Modi

| Modus | Wofür | Kanonisches Ziel-Register |
|-------|-------|---------------------------|
| **A — Definition** | Einen Begriff oder eine Kennzahl eindeutig festlegen (z. B. „Prozessemissionen", „Fluktuationsrate") | `sustainability-development/glossary.md` |
| **B — Ziel** | Ein messbares Ziel/Target setzen (z. B. „Recyclingquote Prozessschrott −X %") | `sustainability-development/targets.yaml` |

Frage zu Beginn, falls unklar: **„Möchtest du etwas *definieren* (Begriff/Kennzahl) oder ein *Ziel* festlegen?"**

---

## Immer zuerst (beide Modi)

1. **Kanonische Quelle prüfen.** Öffne das passende Register (`glossary.md` bzw. `targets.yaml`). Gibt es den Begriff/das Ziel schon? → **bestehenden Eintrag aktualisieren, nicht duplizieren.** (Verhindert die häufigste Inkonsistenz: dasselbe an zwei Stellen.)
2. **ESRS-/Themen-Bezug bestimmen.** Prüfe gegen die wesentlichen Themen (`programs/strategy/materiality/double-materiality-assessment-2026.md`): E1 Klima, E2 Umweltverschmutzung, E5 Ressourcen/Kreislauf, S1 eigene Belegschaft, S2 Wertschöpfungskette, G1 Governance. Ordne den Eintrag einem Thema zu. Passt er zu *keinem* wesentlichen Thema, weise freundlich darauf hin (evtl. nicht berichtspflichtig).
3. **Owner klären.** Jeder Eintrag braucht eine verantwortliche Person. Steht sie nicht fest → nachfragen, nicht raten.

---

## Modus A — Definition

### Pflichtfelder
| Feld | Regel |
|------|-------|
| `begriff` | Der zu definierende Begriff / die Kennzahl |
| `definition` | 1–3 präzise Sätze. Sachlich, keine Marketingsprache. |
| `abgrenzung` | Was der Begriff *nicht* ist / womit er verwechselt wird (z. B. „Prozessemissionen ≠ Prozesswärme-Emissionen") |
| `einheit` | Nur falls Kennzahl — Pflicht, wenn etwas gemessen wird (z. B. tCO₂e, %) |
| `berechnung` | Nur falls Kennzahl — wie wird gerechnet (Formel/Quelle der Aktivitätsdaten) |
| `esrs-bezug` | Zugeordnetes wesentliches Thema / Datenpunkt |
| `synonyme` | Gängige alternative Bezeichnungen (für Auffindbarkeit) |
| `owner` | Verantwortliche Person |
| `stand` | Datum (YYYY-MM-DD) |

### Regeln
- **Eindeutigkeit erzwingen:** Eine Definition, die mehrere Lesarten zulässt, ist nicht fertig — nachschärfen.
- **Kennzahl → Einheit + Berechnung zwingend.** Ohne sie ist die Definition nicht steuerungs-/prüftauglich.
- **Konflikt-Check:** Widerspricht die neue Definition einem bestehenden Begriff im Glossar? Dann auflösen, bevor gespeichert wird.

### Ausgabe (in `glossary.md`, alphabetisch einsortiert)
```markdown
### <Begriff>
- **Definition:** <1–3 Sätze>
- **Abgrenzung:** <was es nicht ist>
- **Einheit / Berechnung:** <falls Kennzahl, sonst „—">
- **ESRS-Bezug:** <Thema/Datenpunkt>
- **Synonyme:** <…>
- **Owner:** <Name> · **Stand:** <YYYY-MM-DD>
```

---

## Modus B — Ziel

### Pflichtfelder
| Feld | Regel |
|------|-------|
| `ziel` | Kurzname des Ziels |
| `metrik` | Was genau gemessen wird, inkl. **Einheit** |
| `baseline_wert` + `baseline_jahr` | Ausgangswert und -jahr — **Pflicht** |
| `zielwert` + `zieljahr` | Zielwert und -jahr |
| `geltungsbereich` | Scope/Standorte/Einheiten, für die das Ziel gilt |
| `esrs_bezug` | Wesentliches Thema / Datenpunkt (z. B. E1-4 Ziele) |
| `massnahmen_bezug` | Welche Initiative(n) zahlen darauf ein (Verweis in `initiative-index.yaml`) |
| `owner` | Verantwortliche Person |
| `status` | z. B. geplant / in Umsetzung |

### Harte Regeln (Vollständigkeit erzwingen)
- 🚫 **Kein Ziel ohne Baseline** (Wert *und* Jahr). Fehlt die Baseline, ist kein seriöses Reduktions-/Quotenziel möglich → schlage stattdessen ein **Fundament-Ziel** vor: *„Baseline für <Metrik> bis <Jahr> erheben"*. (Genau hier scheiterte im Review das E5-Ziel.)
- 🚫 **Keine Metrik ohne Einheit.**
- ⏳ **`zieljahr` > `baseline_jahr`.**
- 🧭 **Plausibilität gegen die Roadmap:** Widerspricht das Ziel der Net-Zero-Roadmap (`programs/strategy/roadmaps/net-zero-roadmap-2030.md`)? Dann markieren und Rückfrage.

### Ausgabe (Eintrag in `targets.yaml`)
```yaml
  - ziel: <Kurzname>
    metrik: <was, inkl. Einheit>
    baseline_wert: <Zahl>
    baseline_jahr: <Jahr>
    zielwert: <Zahl>
    zieljahr: <Jahr>
    geltungsbereich: <…>
    esrs_bezug: <…>
    massnahmen_bezug: <initiative-id oder "noch keine">
    owner: <Name>
    status: <…>
    stand: <YYYY-MM-DD>
```

---

## Interview-Leitfaden (für Nicht-Expert:innen)

Stelle die Pflichtfelder **als einfache Fragen nacheinander**. Fehlende Felder **nicht raten — nachfragen**. Beispiele:

- *HR, das ein S1-Ziel setzen will:* „Welche Kennzahl? (z. B. Unfallrate LTIFR) — Wie hoch ist sie heute und für welches Jahr? — Welchen Wert bis wann?"
- *Procurement, das einen G1-Begriff definieren will:* „Welcher Begriff? — In einem Satz: was bedeutet er bei uns? — Womit wird er oft verwechselt?"

Wenn die Person ein Feld nicht weiß (z. B. ESRS-Bezug), schlage einen Wert vor und lasse ihn bestätigen — übernimm ihn nicht stillschweigend.

---

## Vor dem Speichern: Konsistenz- & Qualitäts-Check

- [ ] Kein Duplikat (bestehendes Register geprüft)
- [ ] Einem wesentlichen Thema zugeordnet (oder Hinweis, dass keins passt)
- [ ] Owner gesetzt (kein Platzhalter)
- [ ] **Modus A:** Definition eindeutig; Kennzahl → Einheit + Berechnung vorhanden
- [ ] **Modus B:** Baseline (Wert + Jahr) vorhanden; Metrik mit Einheit; Zieljahr > Baselinejahr; gegen Roadmap plausibilisiert
- [ ] In das **kanonische Register** geschrieben (nicht in ein beliebiges Dokument)
- [ ] Bei Zielen: Verweis auf einzahlende Initiative gesetzt (oder „noch keine" vermerkt)

## Beispiele

Siehe [examples/beispiele.md](examples/beispiele.md) — je ein vollständiger Definitions- und Ziel-Eintrag.
