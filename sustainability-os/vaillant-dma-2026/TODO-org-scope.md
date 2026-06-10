# TODO — Organisations-Scope (site / segment): aufgeschobene Komplexität

> v1 ist da: Objekttypen `site` + `segment`, Kante `applies_to: [site, segment]` an
> target/kpi/initiative/iro/policy, Hierarchie über `part_of: [segment]`. Damit ist
> „wo / welcher Unternehmensteil" **strukturiert abfragbar** (z. B. Segment-Ziele,
> standortbezogene IROs) — statt nur als `geltungsbereich`-Freitext.
>
> Bewusst NICHT in v1 gebaut (das sind die eigentlichen Komplexitätstreiber):

## 1. Aggregation / Roll-up  (der harte Teil)
Ein Gruppen-Wert als Summe der Standort-Werte (Standort → Segment → Gruppe).
- [ ] Rechenlogik definieren (welche KPIs sind additiv, welche nicht — z. B. Intensitäten/Quoten NICHT).
- [ ] **Doppelzählungs-Schutz**: ein Gruppen-KPI darf nicht mit seinen Standort-KPIs zugleich
      gezählt werden. Klare Regel „Blatt ODER Aggregat", nicht beides.
- [ ] Festlegen, ob das System rechnet oder nur **prüft**, dass die Summe stimmt (Letzteres ist
      sicherer — Assurance statt Berechnung).

## 2. Pflicht-Scoping in den Gates
`applies_to` ist heute optional — bewusst.
- [ ] Regel definieren, **wann** Scope Pflicht ist: konzernweites Ziel = kein Scope nötig;
      Segment-/Standort-Ziel = `applies_to` Pflicht. Das ist Ermessen, kein Automatismus.
- [ ] Falls Pflicht: in `target-gate`/`kpi-gate` als Vertrags-Punkt aufnehmen.

## 3. Migration der `geltungsbereich`-Freitexte
~77 Ziele tragen ein Freitext-Feld `geltungsbereich` (z. B. „Eigenbetrieb (Produktion, F&E,
Fuhrpark)"). Das ist Prosa, nicht abfragbar.
- [ ] Wo ein Text auf einen Standort/ein Segment zeigt: **additiv** die `applies_to`-Kante setzen
      (kein Big-Bang, kein Löschen des Freitexts — er bleibt als Beschreibung).
- [ ] Klären, ob `geltungsbereich` langfristig aus `applies_to` **abgeleitet** werden soll
      (dann wäre es Pflichtfeld-Redundanz) oder als menschliche Beschreibung bestehen bleibt.

## Offene Modellfragen
- **Site-Hierarchie:** gehört ein Standort immer zu genau einem Segment, oder kann er
  (z. B. HQ) mehrere/keines bedienen? (v1 erlaubt 0..n via optionalem `part_of`.)
- **Gruppe als Objekt?** Die Gesamt-Organisation ist heute implizit (= kein `applies_to`).
  Soll es ein explizites Wurzel-Objekt geben, an das Konzern-Ziele hängen?
- **Scope auf Datenpunkten?** `applies_to` ist bewusst nicht an `datapoint` — Offenlegung ist
  i. d. R. konzernweit. Bei Bedarf (standortweise Offenlegung) nachrüsten.

## Bezug zum Bestehenden
- Schema: Typen `site`/`segment`, Kanten `applies_to`/`part_of` in `object-schema.yaml`.
- Freitext-Scope: Pflichtfeld `geltungsbereich` an `target`.
- Demo: `segment-waermeerzeugung`, `site-remscheid` (Vaillant-Instanz).
