---
name: sustainability-standard
description: Standardisierte Definitionen und Ziele für das Sustainability OS formulieren. Einsetzen, wenn jemand (auch aus HR, Procurement oder anderen Fachbereichen) einen Nachhaltigkeits-Begriff bzw. eine Kennzahl definieren oder ein Ziel/Target festlegen will — damit das Ergebnis den OS-Konventionen folgt, vollständig ist und konsistent zu bestehenden Einträgen bleibt.
---

# Skill: Standardisierte Definition oder Ziel

Dieser Skill macht es **jedem Teammitglied — auch ohne Nachhaltigkeits-Fachhintergrund** — möglich, einen Begriff zu definieren oder ein Ziel festzulegen, das sich sauber ins Sustainability OS einfügt. Das Nachhaltigkeitsteam legt die *Konvention* einmal fest (hier); HR, Procurement & Co. bedienen sie selbst. Ergebnis: konsistente, vollständige, prüfsichere Einträge statt verstreuter Definitionen in Köpfen und Mails.

> **Hinweis:** Das OS ist auf das **Objektmodell** umgestellt — jeder Fakt ist genau ein Objekt unter `sustainability-os/object-model/objects/`. Die alten Registries (`targets.yaml`, `glossary.md`) gibt es nicht mehr; ihre Inhalte leben jetzt als `target-*`- und `term-*`-Objekte. Schema: `sustainability-os/object-model/object-schema.yaml`.

## Zwei Modi

| Modus | Wofür | Kanonische Heimat (Objekt-Typ) |
|-------|-------|--------------------------------|
| **A — Definition** | Einen Begriff oder eine Kennzahl eindeutig festlegen (z. B. „Prozessemissionen") | `object-model/objects/term-<id>.md` (`type: term`) |
| **B — Ziel** | Ein messbares Ziel/Target setzen (z. B. „Recyclingquote Prozessschrott −X %") | `object-model/objects/target-<id>.md` (`type: target`) |

Frage zu Beginn, falls unklar: **„Möchtest du etwas *definieren* (Begriff/Kennzahl) oder ein *Ziel* festlegen?"**

---

## Immer zuerst (beide Modi)

1. **Kanonische Quelle prüfen.** Sieh in `object-model/objects/` nach (`term-*` bzw. `target-*`). Gibt es das Objekt schon? → **bestehendes Objekt aktualisieren, nicht duplizieren.** (Verhindert die häufigste Inkonsistenz: dasselbe an zwei Stellen.)
2. **ESRS-/Themen-Bezug bestimmen.** Prüfe gegen die wesentlichen Themen (`object-model/objects/topic-*.md` bzw. `sustainability-development/programs/strategy/materiality/double-materiality-assessment-2026.md`): E1 Klima, E2 Umweltverschmutzung, E5 Ressourcen/Kreislauf, S1 eigene Belegschaft, S2 Wertschöpfungskette, G1 Governance. Setze `esrs_bezug`. Passt der Eintrag zu *keinem* wesentlichen Thema, weise freundlich darauf hin (evtl. nicht berichtspflichtig).
3. **Owner klären.** Jedes Objekt braucht eine `owner`-Person (`person-*`-id). Steht sie nicht fest → nachfragen, nicht raten. Der Validator erzwingt, dass `owner` auf eine existierende Person zeigt.

---

## Modus A — Definition

### Pflichtfelder (Frontmatter + Body)
| Feld | Regel |
|------|-------|
| `begriff` | Der zu definierende Begriff / die Kennzahl (Frontmatter-Pflichtfeld für `type: term`) |
| Definition | 1–3 präzise Sätze im Body. Sachlich, keine Marketingsprache. |
| Abgrenzung | Was der Begriff *nicht* ist / womit er verwechselt wird (z. B. „Prozessemissionen ≠ Prozesswärme-Emissionen") |
| Einheit / Berechnung | Nur falls Kennzahl — Pflicht, wenn etwas gemessen wird (z. B. tCO₂e, %) + wie gerechnet wird |
| `esrs_bezug` | Zugeordnetes wesentliches Thema / Datenpunkt |
| `synonyme` | Gängige alternative Bezeichnungen (für Auffindbarkeit) |
| `owner` | Verantwortliche Person (`person-*`) |
| `stand` | Datum (YYYY-MM-DD) |

### Regeln
- **Eindeutigkeit erzwingen:** Eine Definition, die mehrere Lesarten zulässt, ist nicht fertig — nachschärfen.
- **Kennzahl → Einheit + Berechnung zwingend.** Ohne sie ist die Definition nicht steuerungs-/prüftauglich.
- **Konflikt-Check:** Widerspricht die neue Definition einem bestehenden `term-*`-Objekt? Dann auflösen, bevor gespeichert wird.

### Ausgabe (neue Datei `object-model/objects/term-<id>.md`)
```markdown
---
id: term-<kebab-id>
type: term
owner: person-<id>
status: final
stand: <YYYY-MM-DD>
vertraulichkeit: intern
esrs_bezug: <Thema/Datenpunkt>
begriff: <Begriff>
synonyme: [<…>]
---

# Begriff: <Begriff>

- **Definition:** <1–3 Sätze>
- **Abgrenzung:** <was es nicht ist>
- **Einheit / Berechnung:** <falls Kennzahl, sonst „—">
```

---

## Modus B — Ziel

### Schritt 0 — Kontext über den Object-Model-Pack laden (Pflicht)

**Sammle den Kontext nicht von Hand**, sondern löse den Context-Pack
`sustainability-os/object-model/context-packs/target-setting.pack.yaml`
für das betroffene Thema auf. Konkret:

1. **Topic-Objekt öffnen** (`objects/topic-<thema>.md`) und seine Kanten ablaufen:
   `has_kpi` (aktueller Wert + Trend), `has_target` (bestehende Ziele → Konsistenz!),
   `has_initiative → has_budget` (Hebel + Budget-Restriktion). So kommen die
   bestehenden Ziele/KPIs **frisch aus dem Graphen**.
2. **Eskalations-Klausel anwenden (Pflicht):** Laufe
   `target → measured_by → kpi → at_risk_from → finding WHERE status != geschlossen`
   ab. Findet sich eine **offene Finding, die Baseline oder Metrik berührt**, dann:
   - ⛔ **Kein Ziel auf kippeliger Baseline bestätigen.** Weise auf die Finding hin
     und schlage — passend zur Baseline-Regel unten — ein **Fundament-Ziel** vor
     (*„Baseline für <Metrik> nach Korrektur von <finding> neu berechnen"*).
   - Beispiel: `target-sbti-scope3-2030` zieht über diese Kette
     `finding-2026-05-12-spend-based-overcount` herein → Baseline 2024 erst neu rechnen.
3. **Vertraulichkeit:** Der Pack blendet Objekte oberhalb der Freigabe des Konsumenten
   aus — übernimm diese Grenze (z. B. Budget nicht an Externe weitergeben).

### Pflichtfelder (Frontmatter `type: target`)
| Feld | Regel |
|------|-------|
| `id` | `target-<kebab-id>` |
| `einheit` | Metrik-Einheit (z. B. tCO2e, %) — **Pflicht** |
| `baseline_wert` + `baseline_jahr` | Ausgangswert und -jahr — **Pflicht** |
| `zielwert` + `zieljahr` | Zielwert und -jahr |
| `geltungsbereich` | Scope/Standorte/Einheiten, für die das Ziel gilt |
| `esrs_bezug` | Wesentliches Thema / Datenpunkt (z. B. E1-4) |
| `measured_by` | KPI-Objekt(e), die das Ziel messen (`kpi-*`) |
| `supported_by` | Einzahlende Initiative(n) (`initiative-*`) — oder weglassen, wenn noch keine |
| `owner` | Verantwortliche Person (`person-*`) |
| `status` | z. B. geplant / in-umsetzung |

Zusätzlich: das Ziel beim Thema verlinken (`topic-<thema>.md` → `has_target` ergänzen).

### Harte Regeln (Vollständigkeit erzwingen)
- 🚫 **Kein Ziel ohne Baseline** (Wert *und* Jahr). Fehlt sie → schlage ein **Fundament-Ziel** vor: *„Baseline für <Metrik> bis <Jahr> erheben"*.
- 🚫 **Keine Metrik ohne Einheit.**
- ⏳ **`zieljahr` > `baseline_jahr`.** (Vom Validator erzwungen.)
- 🧭 **Plausibilität gegen die Roadmap:** Widerspricht das Ziel der Net-Zero-Roadmap (`sustainability-development/programs/strategy/roadmaps/net-zero-roadmap-2030.md`)? Dann markieren und Rückfrage.

### Ausgabe (neue Datei `object-model/objects/target-<id>.md`)
```markdown
---
id: target-<kebab-id>
type: target
owner: person-<id>
status: <…>
stand: <YYYY-MM-DD>
vertraulichkeit: intern
esrs_bezug: <…>
einheit: <Einheit>
baseline_wert: <Zahl>
baseline_jahr: <Jahr>
zielwert: <Zahl>
zieljahr: <Jahr>
geltungsbereich: <…>
measured_by: [kpi-<id>]
supported_by: [initiative-<id>]
---

# Ziel: <Kurzname>

<1–2 Sätze Kontext.>
```

---

## Interview-Leitfaden (für Nicht-Expert:innen)

Stelle die Pflichtfelder **als einfache Fragen nacheinander**. Fehlende Felder **nicht raten — nachfragen**. Beispiele:

- *HR, das ein S1-Ziel setzen will:* „Welche Kennzahl? (z. B. Unfallrate LTIFR) — Wie hoch ist sie heute und für welches Jahr? — Welchen Wert bis wann?"
- *Procurement, das einen G1-Begriff definieren will:* „Welcher Begriff? — In einem Satz: was bedeutet er bei uns? — Womit wird er oft verwechselt?"

Wenn die Person ein Feld nicht weiß (z. B. ESRS-Bezug), schlage einen Wert vor und lasse ihn bestätigen — übernimm ihn nicht stillschweigend.

---

## Vor dem Speichern: Konsistenz- & Qualitäts-Check

- [ ] Kein Duplikat (bestehende `term-*`/`target-*`-Objekte geprüft)
- [ ] Einem wesentlichen Thema zugeordnet (`esrs_bezug` gesetzt; oder Hinweis, dass keins passt)
- [ ] `owner` zeigt auf eine existierende `person-*` (kein Platzhalter)
- [ ] **Modus A:** Definition eindeutig; Kennzahl → Einheit + Berechnung vorhanden
- [ ] **Modus B:** Baseline (Wert + Jahr) vorhanden; Einheit gesetzt; Zieljahr > Baselinejahr; gegen Roadmap plausibilisiert; **keine offene Finding kippt die Baseline** (Eskalations-Check aus Schritt 0)
- [ ] Als **Objekt** in `object-model/objects/` angelegt (nicht in ein beliebiges Dokument)
- [ ] Bei Zielen: am Thema verlinkt (`has_target`) und `measured_by`/`supported_by` gesetzt (oder bewusst weggelassen)
- [ ] **`python3 object-model/tools/validate.py` läuft grün** (referenzielle Integrität bestätigt)

## Beispiele

Siehe [examples/beispiele.md](examples/beispiele.md) — je ein vollständiger Definitions- und Ziel-Eintrag.
