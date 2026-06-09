# Tour: In 5 Minuten durch das Sustainability Team OS

> Für Reviewer:innen ohne technischen Hintergrund. Du musst nichts installieren — folge einfach den Links. Am Ende stehen die Fragen, zu denen wir dein Feedback brauchen.

## 0. Worum geht es? (30 Sekunden)

Ein „Team OS" ist eine **geteilte Wissensbasis** eines Nachhaltigkeitsteams — so strukturiert, dass eine KI (oder ein neuer Mensch) sofort versteht, woran das Team arbeitet, ohne dass eine Einzelperson alles erklären muss. Statt Wissen in Köpfen, Mails und verstreuten Dateien liegt der Kontext an *einem* geordneten Ort.

Alle Inhalte hier sind ein **fiktives Beispiel** (Firma „Nordmark Industrie"). Es geht nur um die *Struktur* — die Zahlen sind erfunden.

## 1. Der Einstiegspunkt (1 Minute)

Öffne [`CLAUDE.md`](CLAUDE.md) (im selben Ordner).

Das ist die „Startseite", die jede KI-Session zuerst liest: **Wer im Team ist, welche Kanäle es gibt, wo welche Dokumente liegen, und die Fachbegriffe.** Genau das, was du einer neuen Kollegin am ersten Tag erklären würdest — nur einmal aufgeschrieben.

> 💡 Achte auf die Tabelle „Doc-Index": Sie ist die Landkarte. Jede Zeile führt in einen Bereich.

## 2. Eine Initiative von Anfang bis Ende verfolgen (2 Minuten)

Das Herzstück: Wie hängt alles zusammen? Folge **einer** echten Initiative — „Scope-3-Lieferanten-Engagement" — durch alle Ebenen:

1. **Das „Warum"** → [Brief](sustainability-development/programs/briefs/scope-3-supplier-engagement/scope-3-supplier-engagement-brief.md): Problem, Ziel, Erfolgsmetrik.
2. **Das „Wie"** → [Umsetzungsplan](sustainability-development/implementation/plans/scope-3/supplier-data-collection.md): Arbeitspakete, wer macht was.
3. **Die Daten** → [Emissionsfaktoren](object-model/objects/) (`ef-*`-Objekte) und [THG-Inventar](sustainability-development/carbon-data/inventory/ghg-inventory-2025.md): die Zahlen dahinter.
4. **Ein Problem** → [Datenqualitäts-Finding](sustainability-development/implementation/data-quality-findings/scope-3/2026-05-12-spend-based-overcount.md): ein dokumentierter Datenfehler und seine Korrektur.
5. **Das Reporting** → [ESRS-Datenpunkt-Mapping](sustainability-development/reporting/esrs-datapoint-mapping.md): wie dieselbe Initiative in die CSRD-Offenlegung fließt.

> 💡 Das ist der Kern: Eine Initiative ist *kein* einzelnes Dokument, sondern ein roter Faden durch Strategie → Umsetzung → Daten → Reporting. Das [`initiative-*.md`-Objekt](object-model/objects/) im Objektmodell verknüpft das alles über Objekt-Kanten an einer Stelle.

## 3. Der Praxistest (1,5 Minuten) — optional, wenn KI zur Hand

Der eigentliche Wert zeigt sich, wenn eine KI mit diesem OS arbeitet. Stell (in einer KI-Session, die auf dieses Repo Zugriff hat) eine echte Arbeitsfrage, z. B.:

> *„Was ist unser größter Hebel zur Scope-3-Reduktion und welches Datenproblem steht dem im Weg?"*

Eine gute Antwort sollte ohne weitere Erklärung das Lieferanten-Engagement, den spend-based-Charakter der Daten und das Doppelzählungs-Finding nennen — gezogen aus den verlinkten Dateien. **Das** ist der Test: Kontext ist self-service, nicht an eine Person gebunden.

## Womit wir dein Feedback brauchen

Bitte reagiere auf diese vier Punkte — sie steuern, wie wir weitermachen:

1. **Mentales Modell:** Entspricht die oberste Gliederung (Programme · Carbon Data · Implementation · Reporting) der Art, wie *du* die Arbeit denkst? Was würdest du anders schneiden?
2. **Vollständigkeit:** Welcher Bereich, den dein Team täglich braucht, fehlt komplett?
3. **Über-/Untergewichtung:** Wo ist zu viel Struktur (Overhead), wo zu wenig?
4. **Adoption:** Was wäre nötig, damit dein Team das wirklich pflegt statt verfallen lässt? (Mehr dazu in [`MAINTAINING.md`](MAINTAINING.md).)

> Notiere Antworten formlos — Stichpunkte reichen. Daraus leiten wir die nächste Iteration ab.
