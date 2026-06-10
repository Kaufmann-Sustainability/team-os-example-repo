# TODO — Effiziente Such-/Navigationslogik (Scope vor Traversierung)

> **Problem.** Jede Frage lädt heute faktisch **alle ~690 Objekte** und filtert sie per ad-hoc-Skript
> (Full-Scan). Das ist token-teuer und brüchig (hängt an Namenskonventionen wie `iro-e1-*`).
> Beobachtet an den letzten Live-Fragen: „Maßnahmen im Bereich Klima", „Owner X in Klima",
> „IROs im Klima" — jedes Mal Vollscan, obwohl nur ein kleiner Ausschnitt relevant war.

> **Ziel.** Erst den **Scope erkennen**, dann **nur diesen Ausschnitt** anfassen:
> - „ah, es geht um **topic Klima**" → nur E1-Objekte laden
> - „ah, es geht um **Owner X in Klima**" → nur E1 ∩ owner=X
> Kein Objekt wird gescreent, das nicht in den erkannten Scope fällt.

## Zielarchitektur: Retrieval-Planner + Index

```
NL-Frage
   │  1) INTENT-/SCOPE-RESOLVER  → {standard/topic, typ, owner?, anker?, kante?}
   ▼
   │  2) INDEX-LOOKUP (kein File-Scan) → Kandidaten-ids im Scope
   ▼
   │  3) GEZIELTES LADEN nur dieser Objekte → Kanten-Walk (pack/topic-View)
   ▼
Antwort  (Token-Verbrauch ∝ Scope, nicht ∝ Graph-Größe)
```

## Arbeitsschritte

### 1. Leichtgewichtiger Index (Voraussetzung)
- [ ] `tools/build_index.py`: erzeugt `reference/objects-index.json` mit je Objekt nur den
      Navigationsfeldern: `id, type, standard, topic, owner, status, edges{kante→[ziel-ids]}`.
- [ ] Frisch halten: Index-Build an `validate.py` koppeln oder als Pre-Commit; Stale-Check.
- [ ] Damit beantwortbar **ohne** Markdown zu öffnen: „alle `initiative` in `E1`",
      „alle Objekte mit `owner=X` in `topic=klima`".

### 2. Intent-/Scope-Resolver
- [ ] Mapping NL → Scope-Filter, deterministisch wo möglich:
      - Thema/Bereich („Klima"→E1, „Belegschaft"→S1, …) aus den `topic`-Objekten, **nicht** hardcodiert.
      - Objekt-Typ aus Schlüsselwörtern („Maßnahmen"→initiative, „Ziele"→target, „Kennzahl"→kpi,
        „Risiken/Chancen/Auswirkungen"→iro).
      - Owner/Person aus dem Team-Roster.
- [ ] Output ist ein **Scope-Filter** `{standard?, topic?, type?, owner?}` + optional Anker-id +
      zu folgende Kante — der Plan, *bevor* irgendetwas geladen wird.
- [ ] Synonyme/Aliase pflegen (Eigenbetrieb→Scope 1+2→iro-e1-i2), damit NL nicht am Schema-Wissen klebt.

### 3. Scoped Retrieval statt Full-Scan
- [ ] `query.py` so umbauen, dass es den Scope-Filter auf den **Index** anwendet und nur die
      gefilterten Objekte materialisiert (Markdown erst beim finalen Hop öffnen, wenn Volltext nötig).
- [ ] Harte Regel: **nie den ganzen `objects/`-Ordner laden**, wenn ein Scope-Filter vorliegt.

### 4. Native Views als Traversierungs-Primitive nutzen
- [ ] Bestehende `pack target-setting` / `pack dma` / `my-work` / `topic`-Objekte konsequent als
      Einstiegspunkte verwenden, statt jede Traversierung ad-hoc neu zu schreiben.
- [ ] Fehlende Views ergänzen (z. B. `pack ownership <person>` bereits ~`my-work`; ggf. `by-topic <topic> <typ>`).

### 5. Token-/Effizienz-Budget
- [ ] Messung einbauen: „Frage X → N Objekte geladen / M Tokens" als Telemetrie, um Vollscans zu erkennen.
- [ ] Zielmetrik: geladene Objekte ≈ Größe des relevanten Subgraphen, **nicht** Gesamtgraph.

## Beispiele (Soll-Verhalten)
| Frage | erkannter Scope | geladen (statt 690) |
|-------|-----------------|---------------------|
| „Maßnahmen im Bereich Klima" | `topic=E1, type=initiative` | ~8 Initiativen |
| „Wofür ist Head of Decarb verantwortlich?" | `owner=person-…-decarb` | nur dessen Objekte |
| „IROs im Klima" | `topic=E1, type=iro` | 23 IROs |
| „Ziele/Maßnahmen Eigenbetrieb Scope 1+2" | Alias→`anker=iro-e1-i2`, Kanten `addresses⁻¹→supported_by` | 1 Ziel + 1 Maßnahme |

## Bezug zum Bestehenden
- Heutiger Zugriff: `tools/query.py` (lädt alle Objekte, filtert in Python).
- Navigationsfelder liegen schon im Frontmatter (`type`, `concerns→topic`, `owner`, `esrs_bezug`) —
  müssen nur **indexiert** statt jedes Mal neu gescannt werden.
- Verwandtes TODO: `TODO-ownership-rasci.md` (Owner/Rollen sind ein zentrales Scope-Kriterium).
