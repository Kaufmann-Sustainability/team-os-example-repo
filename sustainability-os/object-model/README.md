# Object-Model — die kanonische Wissensschicht des Sustainability OS

> **Was das ist:** Das **kanonische** Objektmodell des OS. Jeder Fakt ist genau ein
> Objekt unter `objects/`; Sichten (`views/`) und Context-Packs (`context-packs/`) lesen
> daraus, kopieren nicht. Validiert von `tools/validate.py`, in CI erzwungen.
>
> Erprobt wurde es an drei vertikalen Durchstichen — alle drei tragen:
> 1. **Target-Setting** — *ein Ziel für ein Thema setzen* (strukturlastig).
> 2. **DMA** — *Wesentlichkeit eines Themas bestimmen/verteidigen* (narrativlastig, härtere Probe).
> 3. **Disclosure/Assurance** — *einen ESRS-Datenpunkt prüfsicher offenlegen* (schließt die
>    Reporting-/Prüf-Lücken #17/#18/#19).
>
> **Status:** Kanonisch (voller Umzug umgesetzt). Die früheren Registries
> (`targets.yaml`, `glossary.md`, `initiative-index.yaml`, EF-Katalog) sind in Objekte
> migriert und gelöscht; ihre Inhalte leben hier als `target-*`, `term-*`, `initiative-*`,
> `kpi-*` und `ef-*`. Im Doc-Index der Root-`CLAUDE.md` verlinkt.

## Woher die Idee kommt
Drei Evolutionsschritte führten hierher: **(1)** Domänen-Taxonomie → **(2)** Objekte +
Beziehungen + Views → **(3)** Context Packs (minimal context retrieval, à la Hannahs
Team OS). Dieser Spike realisiert Schritt 2 + 3 an einem Beispiel. Die zugrunde
liegenden Probleme stehen in [`../REVIEW-SYNTHESIS.md`](../REVIEW-SYNTHESIS.md) (5 Grundprobleme A–E).

## Die 4 Schichten → wo sie hier liegen

| Schicht | Frage | Hier |
|---------|-------|------|
| **Knowledge** | Was existiert? Wie verbunden? | `objects/` (je Objekt eine Datei mit ID + getypten Kanten), `object-schema.yaml` |
| **Retrieval** | Welcher Minimal-Kontext? Wer schaut? | `context-packs/*.pack.yaml` (Pack = Query), `views/*.view.yaml` |
| **Execution** | Was wird getan, von wem? | Objekt-Felder `status`/`owner` + `initiative`-Objekt + `at_risk_from`-Kanten |
| **AI** | Wie nutzt ein Agent das? | `sustainability-standard`-Skill konsumiert den Pack (s. u.); `triggers/` |

## Das Beispiel (echte Daten, kein Fantasie-Set)
Ziel **SBTi Near-Term Scope 3** (`target-sbti-scope3-2030`) — ursprünglich aus dem
inzwischen migrierten `targets.yaml`, jetzt kanonisch als Objekt — mit seinem KPI, der
einzahlenden Initiative, Budget, Freigabe-Entscheidung und dem **realen**
Datenqualitäts-Finding `finding-2026-05-12-spend-based-overcount`.

## Was der Spike beweist (gegen die 5 Grundprobleme)

- **A — Single Source of Truth:** Jedes Objekt existiert **einmal** (`objects/`); Views/Packs
  *referenzieren*, kopieren nicht. Owner/Status sind Felder, keine Prosa → die Owner-Frage
  („Wofür ist Jonas verantwortlich?") wird zuverlässig (`views/my-work.view.yaml`).
- **C — Lebenszyklus-Artefakte:** `decision-…` (trägt Begründung), `finding-…` (Prüf-/Risiko-Spur)
  existieren als erstklassige Objekte — nicht mehr nur Briefs + Bug-Findings.
- **D — Governance:** Jedes Objekt trägt `stand`, `review_zyklus`, `vertraulichkeit`.
  Vertraulichkeit + Minimal-Retrieval sind **derselbe** Mechanismus (Pack-Filter blendet
  `budget-…` für Externe aus). Frische wird abfragbar → Refresh-Trigger.
- **E — Konsistenz erzwungen, nicht erhofft:** `tools/validate.py` prüft Pflichtfelder,
  tote Kanten, Ziel-Regeln, Frische. Lauffähig, exit≠0 bei Fehler (CI-tauglich).

### Der eigentliche Beweis: die Eskalations-Klausel
Der Target-Setting-Pack **schließt** `type: finding` (Berechnungsdetails) **aus** — und
zieht über die `eskalation_immer_einschliessen`-Regel doch genau das spend-based-Finding
herein, weil es die **Baseline kippt**. So wird „minimal" nicht „lückenhaft": Ein materieller
Ausschluss ist teurer als etwas Rauschen. Das ist die Antwort auf die Schwäche, die reine
Ausschlusslisten sonst hätten.

## So nutzt der `sustainability-standard`-Skill das (AI Layer)
Heute baut der Skill (Modus B — Ziel setzen) seinen Kontext implizit. Mit dem Objektmodell
**konsumiert** er stattdessen den Pack:

| Skill-Schritt (heute) | Mit Objektmodell |
|-----------------------|------------------|
| „Kanonische Quelle prüfen" | Lade `target-setting.pack` für `{topic_id}` → bestehende Targets/KPIs kommen frisch aus dem Graph |
| „Plausibilität gegen Roadmap" | Pack liefert die Roadmap-Referenz als `ref` |
| (Lücke heute) Baseline-Risiko | **Eskalations-Klausel** liefert offene Findings automatisch → „kein Ziel auf kippeliger Baseline" |
| „Owner klären / nicht raten" | `owner`-Feld ist Pflicht + von `validate.py` erzwungen |

→ Der Skill hört auf, Kontext fest einzubauen; er fragt den Graphen. Genau hier treffen
sich Hannahs „minimal context" und das Objektmodell.

## Zweiter Durchstich: DMA (die härtere Probe)
Die DMA stresst das Modell bewusst stärker — und es hält. Was sie zeigt:

- **Narrativ-in-Objekten trägt.** Die Wesentlichkeits-*Begründung* (Impact/finanziell)
  lebt als Fließtext im Body der `iro-…`-Objekte; die *Scores* als strukturierte Felder
  (`impact_wesentlichkeit`, `finanz_wesentlichkeit`, `wesentlich`). Beides nebeneinander
  funktioniert — Prosa für das Warum, Felder für die Query.
- **Das „nicht wesentlich"-Urteil bekommt eine Heimat.** `topic-e3-wasser` + `iro-e3-wasser`
  existieren als vollwertige Objekte *mit Begründung* — denn Auditoren fechten gerade die
  **Ausschlüsse** an. Im alten OS gab es für ausgeschlossene Themen schlicht keinen Ort.
- **Neue Objekt-Typen, gleiches Muster:** `iro`, `stakeholder`, `methodology`, `threshold`.
  Methodik + Schwellwert als eigene Objekte machen *„nach welcher Regel wurde entschieden?"*
  in einem Hop beantwortbar (Begründungs-Layer, Grundproblem C/D).
- **Themen-Objekte akkumulieren Kanten über Aufgaben hinweg:** `topic-e1-klima` trägt jetzt
  `has_target` (aus Slice 1) **und** `has_iro` (aus Slice 2) — ein Objekt, viele Aufgaben.
- **Grundproblem B wird sichtbar:** `topic-e2-umwelt` ist wesentlich, aber **hohl**
  (nur `has_iro`, kein `has_target`). Eine Query „wesentlich ohne Ziel" findet die Lücke sofort.

### DMA-Eskalations-Klausel (anderer Fall als Target-Setting)
Bei der DMA ist der teure Fehler nicht „zu viel Kontext", sondern ein **stillschweigender
Ausschluss**. Der `dma.pack` liefert deshalb bei einem *nicht-wesentlichen* Thema **immer**
(a) die Ausschluss-Begründung und (b) jeden **widersprechenden** Stakeholder-Input mit.
Konkret: Für `topic-e3-wasser` zieht er den **Investoren-Dissens** (Wasser als aufkommendes
Risiko) herein — damit der Ausschluss bei der nächsten Prüfung verteidigt oder revidiert
wird, statt im Stillen zu veralten. Das `review_zyklus: P6M` auf dem IRO sorgt zusätzlich
dafür, dass der Refresh-Sweep ihn früher wieder hochspült.

## Dritter Durchstich: Disclosure / Assurance (schließt #17/#18/#19)
Modelliert die Offenlegung eines Datenpunkts — die Schicht, die im alten OS ganz fehlte:

- **Versionierter Berichtstext (#19):** `disclosure-e1-6-2025` trägt `berichtsjahr` + `version`
  + den eigentlichen Wortlaut im Body. Der Bericht ist ein *Objekt*, keine verstreute Word-Datei.
- **Pflicht vs. Erfüllung getrennt:** `datapoint` (die ESRS-Anforderung) ↔ `disclosure` (der
  erfüllte Text). Ein Datenpunkt ohne finale Disclosure ist ein **abfragbarer Reporting-Gap**.
- **Prüfspur (#17):** `evidence` (`backs` → disclosure) und `control` (`covers` → datapoint).
- **Audit-Feedback (#18):** eigener Typ `audit-finding` (`challenges` → disclosure) — Prüfer-
  Beanstandung, getrennt von eigenen Datenqualitäts-Findings.

### Der stärkste Beweis des ganzen Spikes: eine Tatsache, drei Aufgaben
Das spend-based-Finding (`finding-2026-05-12-spend-based-overcount`) kippt die Scope-3-Baseline.
Dieselbe **eine** Tatsache taucht jetzt in **drei** Aufgaben auf, weil alle zum selben
`kpi-scope3-intensitaet`-Objekt traversieren:
1. **Target-Setting** → „kein Ziel auf kippeliger Baseline".
2. **Disclosure** → KPI vorläufig, Offenlegung kann nicht final werden.
3. **Assurance** → der Auditor beanstandet exakt dieselbe Baseline-Konsistenz (`audit-finding-…`).

Im alten OS lag diese Tatsache in *einer* Datei und wäre in den anderen zwei Kontexten
unsichtbar geblieben. Hier ist sie **einmal** modelliert und über Kanten **überall** präsent.
Das ist „Objekte existieren einmal, Kontext ist verbunden" — am konkreten Fall.

### Disclosure-Eskalation = ein Gate
Der `disclosure.pack` ist ein **Freigabe-Gate**: Eine Offenlegung darf `final`/`assured` nicht
erreichen, solange (a) eine offene Datenqualitäts-Finding den berichteten KPI berührt oder
(b) ein offenes Audit-Finding sie beanstandet. Beide werden immer mitgeliefert — auch wenn der
Konsument „nur den Text" wollte. *Nichts veröffentlichen, was du nicht beweisen kannst.*

## Die Loop-/Refresh-Frage (Pflege als Feature)
Siehe `triggers/quarterly-refresh.md` + `context-packs/refresh-sweep.pack.yaml`:
Ein **geplanter Trigger** (nicht `/loop` — Container sind ephemer) fährt quartalsweise
den Sweep und fragt Owner gezielt: *„Gab es seit Q1 neue Klima-Maßnahmen, die in
`initiative-scope3-supplier-engagement` fehlen?"* — macht aus dem Adoptions-Risiko ein System.

## Selbst ausprobieren
```bash
cd sustainability-os/object-model
python3 tools/validate.py        # erwartet: ✓ Integrität OK
```
Zum Gegentest: in einem Objekt eine Kanten-ID verfälschen → `validate.py` meldet die tote Kante (exit 1).

## Wo es (ehrlich) hakt — was der Spike sichtbar macht
- **Narrativ-in-Objekten:** Durch DMA *und* Disclosure getestet — **hält**. Body = Begründung/
  Berichtstext (Prosa), Frontmatter = Scores/Version/Kanten. Caveat: Sehr lange, mehrteilige
  Narrative (volle DMA-Doku, Methodik-Handbuch) wollen perspektivisch ein eigenes Doc-Objekt,
  das das IRO/die Disclosure *referenziert*, statt alles in einen Body zu pressen.
- **Views sind nicht gratis:** `my-work.view.yaml` ist eine *Spezifikation* — sie zu
  rendern braucht Tooling (oder die KI generiert sie on demand). Im Repo gibt es keine
  Klick-Oberfläche.
- **Wer pflegt's?** Das echte Risiko. Der Refresh-Trigger mildert, ersetzt aber nicht den
  Owner, der antwortet.
- **Doppelung Graph ↔ Ordnerwelt:** ~~offen~~ **gelöst** — die Registries wurden migriert und
  gelöscht; KPI/Target leben jetzt nur noch *einmal* (als Objekt). Verbleibende Rohdaten
  (Inventar) bleiben als referenzierte Datenquelle, nicht als konkurrierende Wahrheit.
- **Lange Narrative** wollen perspektivisch ein referenziertes Doc-Objekt statt alles im Body.

## Status der Bau-Entscheidung
Die Bau-Frage (`DECISION-build-vs-view.md`) wurde zugunsten **Option A (Graph kanonisch)**
entschieden und umgesetzt: voller Umzug der Registries in Objekte. Offene Folgeschritte:
1. Refresh-Trigger (quartalsweise) real einrichten — Pflege der ~lebendigen Objekte.
2. Weitere Themen (E2/E5/S1/S2/G1) über die hohlen Topic-Objekte hinaus ausmodellieren.
3. View-Rendering (KI-generiert) für die menschlichen Sichten.
