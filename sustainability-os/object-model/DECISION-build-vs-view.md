# Entscheidungsvorlage: Wird der Objektgraph kanonisch — oder bleibt er generierte Sicht?

**Owner:** Head of Sustainability · **Stand:** 2026-06-09 · **Status:** ENTSCHIEDEN
**Entscheider:** Sustainability Leads (Lena, Markus, Aylin)

> **✅ Beschluss (2026-06-09): Option A — Graph kanonisch.** Im Test-Kontext umgesetzt:
> voller Umzug der Registries (`targets.yaml`, `glossary.md`, `initiative-index.yaml`,
> EF-Katalog) in Objekte; die Registries wurden gelöscht. Damit ist der Objektgraph die
> einzige Schreib-Heimat. Die ursprüngliche Empfehlung (unten) lautete Option C (Hybrid) —
> bewusst überstimmt, weil dies ein Demo-/Test-Repo ist und der saubere Endzustand den
> höheren Lehrwert hat. Die Optionen/Trigger bleiben als Dokumentation der Abwägung erhalten.

---

## Worum es ging

Das Objektmodell hat an **drei** Aufgaben gezeigt, dass es trägt:
Target-Setting (struktur-), DMA (narrativ-), Disclosure (prüfungslastig). 29 Objekte, Validator grün, CI aktiv.
Bevor wir es ausweiten, ist **eine** Frage zu klären:

> **Lebt die Wahrheit künftig in den Objekten — oder bleiben die bestehenden Registries
> (`targets.yaml`, `glossary.md`, `initiative-index.yaml`, Inventar) die Wahrheit, und die
> Objekte sind nur eine daraus erzeugte Sicht?**

Jeder Fakt braucht **genau eine** kanonische Heimat (Grundproblem A). Diese Entscheidung legt fest, *welche*.

---

## Optionen

| | **A — Graph kanonisch** | **B — Graph als Sicht** | **C — Hybrid (phasiert)** |
|---|---|---|---|
| **Wahrheit** | `objects/` | bestehende Registries | Registries für Bestehendes, Graph für Neues |
| **Registries** | werden migriert & abgelöst | bleiben, unverändert | bleiben kanonisch, werden *projiziert* |
| **Neue Typen** (Decision, IRO, Disclosure, Evidence, Control, Audit-Finding, Stakeholder) | im Graph | bräuchten erst noch eine Heimat | **im Graph kanonisch** |
| **Aufwand jetzt** | hoch (Migration + Editier-Tooling) | niedrig, aber Neu-Typen bleiben heimatlos | mittel (1 Generator + Konventions-Grenze) |
| **Reversibel** | schwer zurück | leicht | leicht je Klasse |
| **Risiko** | reißt eine *gelöste* Sache (Registries) wieder auf | löst die eigentliche Lücke (Lebenszyklus-Typen) **nicht** | Grenze Registry↔Graph muss diszipliniert sein |

---

## Empfehlung: **Option C — Hybrid, phasiert**

**Begründung:**
1. Die Registries lösen Grundproblem A für *ihre* Fakten bereits — und der `sustainability-standard`-Skill
   schreibt schon hinein. Das wegzuwerfen (Option A) bekämpft eine **gewonnene** Schlacht neu.
2. Die echte Lücke waren die **Lebenszyklus-Typen** (Decisions, IROs, Disclosures, Evidence, Audit-Findings).
   Die haben *heute keine kanonische Heimat* — für sie soll der **Graph kanonisch** werden.
3. Registries sind bereits *halb-relational* (`massnahmen_bezug`, `esrs_bezug` sind faktisch Kanten) — ein
   Generator kann daraus read-only-Objekte projizieren, ohne dass jemand doppelt pflegt.

**Die eine Regel, die C zusammenhält:**
> Jeder Fakt hat genau eine Schreib-Heimat. Registry-Fakten werden **nur** in der Registry editiert
> (Graph-Objekt ist read-only-Projektion); Lebenszyklus-Objekte werden **nur** im Graph editiert.
> Der Validator prüft die Grenze mit.

---

## Was C konkret heißt (nächste Schritte)

1. **Generator schreiben:** liest `targets.yaml`/`glossary.md`/`initiative-index.yaml`/Inventar → erzeugt
   `objects/`-Projektionen (markiert `quelle:` + `read_only: true`).
2. **Neu-Typen kanonisch im Graph** belassen (wie im Spike: decision/iro/disclosure/evidence/control/audit-finding/stakeholder).
3. **Validator erweitern:** read-only-Projektionen dürfen nicht von Hand geändert werden (Drift-Check gegen die Registry).
4. **Ein zweites Thema voll** ausmodellieren (z. B. E5 Kreislauf), um die Mengen/Pflege real zu messen.
5. **Refresh-Trigger** (quartalsweise) auf die ~80 lebendigen Objekte scharf schalten.

---

## Trigger, die die Empfehlung kippen würden

- **→ Option A**, wenn ihr später auf ein echtes Datensystem (Notion/Graph-DB/App) geht — dann wird der Graph
  ohnehin Schreib-Heimat, und die Registries wandern hinein.
- **→ Option B**, wenn das Team Tooling minimal halten will und die neuen Lebenszyklus-Typen vorerst *nicht*
  braucht (reines Carbon-/Ziel-Reporting) — dann lohnt der Graph als kanonische Schicht noch nicht.

---

## Offene Punkte vor Freigabe
- Wer baut & pflegt den Generator (Schritt 1)? (Data Analyst — Mira?)
- Akzeptieren wir read-only-Projektionen, oder soll perspektivisch *alles* in den Graph?
- Budget/Zeit für die Ausweitung auf alle 6 Themen (~200 Objekte, ~80 davon lebendig).
