# TODO — Ownership & RASCI für Verantwortlichkeiten

> Ausgelöst durch den `my-work`-Lauf: 37 Berichts-Datenpunkte hingen plötzlich am Head of
> Decarbonization — automatisch zugewiesen, ohne dass er davon weiß. Zwei zusammenhängende
> Baustellen: **(A) keine stille Owner-Zuweisung** und **(B) RASCI statt einzelnem `owner`.**

## A) Owner für Berichtspflichten nie automatisch verteilen — formales Handover nötig

**Problem.** `tools/gen_datapoints.py` setzt `owner` aus einer `OWNER_MAP` automatisch beim Minten.
Dadurch wurde eine Person faktisch für 37 Offenlegungspflichten verantwortlich gemacht, ohne
Kenntnis oder Zustimmung. Verantwortung darf nicht aus einem Skript „entstehen".

**Anforderung.** Eigentum an einer Berichtspflicht entsteht **nur durch ausdrückliche, bestätigte
Übergabe** — nie als Default eines Generators.

- [ ] Generator vergibt **keinen realen Personen-Owner** mehr per Default; stattdessen
      `owner: person-unassigned` (Platzhalter) **oder** Feld `vorgeschlagener_owner` +
      `owner_status: offen`.
- [ ] **Handover-Objekt** einführen (analog `approval`): `handover` mit `datum`, `von`, `an`,
      `bestätigt_von` und Kante `assigns: [datapoint/…]`. Ein Owner gilt erst nach Bestätigung.
- [ ] Regel in `validate.py` (Warnung): Objekt mit realem Owner, aber **ohne** zugehöriges
      bestätigtes Handover → „nicht freigegebene Verantwortung".
- [ ] `my-work` kennzeichnet **vorgeschlagene vs. bestätigte** Zuständigkeit getrennt, damit
      niemand stillschweigend in einer Arbeitsliste auftaucht.
- [ ] Bestehende 37 auto-zugewiesenen Datenpunkte rückwirkend auf `offen` setzen, bis bestätigt.

## B) RASCI konsequent implementieren

**Problem.** Das einzelne Feld `owner` vermischt **Rechenschaft** (wer steht gerade) mit
**Umsetzung** (wer macht es). Beispiel: Bei manchen Maßnahmen ist der Head of Decarbonization
formell **accountable**, die Umsetzung liegt aber **bei jemand anderem** (Werkleitung, Portfolio,
Procurement). Das ist heute nicht abbildbar.

**Anforderung.** RASCI als getypte Rollen-Kanten, statt eines einzelnen Owners.

| Rolle | Bedeutung | Kardinalität |
|-------|-----------|--------------|
| **R**esponsible | führt die Umsetzung aus | ≥1 |
| **A**ccountable | trägt die Rechenschaft (genau einer) | genau 1 |
| **S**upport | liefert Zuarbeit/Ressourcen | 0..n |
| **C**onsulted | wird vorher gefragt (Zwei-Wege) | 0..n |
| **I**nformed | wird informiert (Ein-Weg) | 0..n |

- [ ] `object-schema.yaml`: Rollen-Kanten `accountable_*`/`responsible_*`/`consulted`/`informed`/
      `supports_role` (Namensschema festlegen) → Zieltyp `person`; mindestens für
      `target`, `initiative`, `datapoint`, `policy`.
- [ ] Verhältnis zu `owner` klären: `owner` = `accountable` (Rückwärtskompatibilität, genau 1)
      und `owner` als Alias deprecaten **oder** sauber migrieren.
- [ ] `validate.py`: genau **ein** Accountable je Objekt; R/A/C/I zeigen auf existierende `person`.
- [ ] Gates erweitern (`target-gate`, `initiative-gate`): „Accountable gesetzt **und** ≥1
      Responsible" als Pflicht; Accountable ≠ Responsible explizit erlaubt und sichtbar.
- [ ] `my-work` nach Rolle aufschlüsseln: „accountable für …", „responsible für …", „consulted bei …".
- [ ] Initiativen-Beispiel sauber abbilden: Head of Decarb = **Accountable**, ausführende
      Stelle = **Responsible** (heute fälschlich beides im `owner`).

## Zusammenhang
A und B greifen ineinander: Das **Handover** (A) ist der Akt, der eine Person zur
**Accountable/Responsible** (B) macht — mit Bestätigung, Datum und Spur. Kein Rollenwechsel ohne
bestätigtes Handover.

## Bezug zum Bestehenden
- Auto-Zuweisung: `tools/gen_datapoints.py` (`OWNER_MAP`, `OWNER_DEFAULT`).
- Owner-Regel & Integrität: `tools/validate.py` (owner → existierende person).
- Sichten: `tools/query.py` (`my-work`).
- Vertrags-Gates: `.claude/skills/{target-gate,initiative-gate,…}`.
