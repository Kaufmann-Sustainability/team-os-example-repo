# TODO — Duplikate vermeiden (Dedup vor Anlage)

> **Problem.** Nichts verhindert, dass dasselbe Sachobjekt **zweimal** entsteht. Real passiert im
> target-gate-Test: zwei Energieintensitäts-Ziele nebeneinander (`100→80` UND `100→70`), beide
> valide, beide im Graph. Klassischer Mehr-Nutzer-Fall: A legt ein Ziel an, B kennt es nicht und
> legt es nochmal an. `validate.py` prüft nur referenzielle Integrität + Datei-id-Eindeutigkeit —
> **semantische Dubletten rutschen durch.**

> **Ziel.** Bevor ein Objekt angelegt wird, erkennt das System „so etwas gibt es schon" und fragt:
> **neues Objekt** oder **bestehendes aktualisieren**? Bestehende Dubletten werden auffindbar.

## Bausteine

### 1. Natürlicher Schlüssel je Objekttyp
- [ ] Pro Typ einen **Dedup-Key** definieren (nicht die zufällige id):
      - `target`  : adressierte IRO(s) + `einheit` + `geltungsbereich` (+ Zieljahr-Nähe)
      - `kpi`     : `einheit` + gemessenes Target / Konzept (+ Name normalisiert)
      - `iro`     : `sub_thema` + Wertschöpfungsketten-Position + Kern der Beschreibung
      - `policy`/`initiative`: betroffenes Thema + Geltungsbereich/Scope
- [ ] Normalisierung (Kleinschreibung, Synonyme, Trim) für den Vergleich.

### 2. Dedup-Check bei der Anlage (Gate-Schritt 0)
- [ ] Jeder Anlege-Skill (`target-gate`, `kpi-gate`, `iro-gate`, …) startet mit:
      „existiert ein Objekt mit gleichem/ähnlichem Dedup-Key?" → Kandidaten zeigen.
- [ ] Pflicht-Entscheidung des Nutzers: **(a) wirklich neu**, **(b) das bestehende aktualisieren**,
      **(c) Variante mit explizitem Unterscheidungsmerkmal** (warum es kein Duplikat ist).
- [ ] Ergebnis dokumentieren (z. B. `abgegrenzt_von: [target-…]`), damit „bewusst zwei" nachvollziehbar ist.

### 3. Detektor für bestehende Dubletten
- [ ] `tools/dedupe_check.py` bzw. `query.py duplicates`: scannt je Typ nach Key-Kollisionen und
      Beinah-Treffern (gleiche IRO + gleiche Einheit; KPIs mit gleichem Namen; IROs gleiches
      sub_thema + ähnliche Beschreibung).
- [ ] Als **Warnung** in `validate.py` einhängen (kein harter Fehler — manchmal sind zwei legitim).
- [ ] Sofort-Nutzen: die Energieintensitäts-Dublette aus dem Test aufspüren und bereinigen.

### 4. Mehr-Nutzer-Sicht
- [ ] Bei „jemand anders legt dasselbe an": Dedup-Check zeigt **wer** das bestehende Objekt besitzt
      (owner) → Verweis auf Abstimmung statt stiller Zweitanlage.
- [ ] Zusammenspiel mit Handover/RASCI: Zweitanlage ist oft eigentlich ein Übernahme-/Update-Wunsch.

## Bezug zum Bestehenden
- `validate.py` (heute nur Integrität, kein Dedup) — natürlicher Ort für die Warnung.
- Gate-Skills `.claude/skills/*-gate` — natürlicher Ort für den Anlage-Check (Schritt 0).
- Effizienz: nutzt denselben **Index/Scope-Resolver** wie `TODO-suchlogik-navigation.md`
  (Dedup-Suche darf nicht den ganzen Graphen scannen).
- Sofort-Fall: zwei `target-e1-energieintensitaet…`-Ziele (100→80 vs. 100→70) bereinigen.
