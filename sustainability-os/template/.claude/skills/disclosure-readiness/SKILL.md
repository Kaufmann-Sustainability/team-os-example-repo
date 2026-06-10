---
name: disclosure-readiness
description: Release-Gate vor der Offenlegung. Einsetzen, wenn ein Thema für den CSRD/ESRS-Bericht freigegeben werden soll — prüft, ob der Apparat steht, jeder ESRS-Datenpunkt eine Offenlegung hat, jede berichtete KPI aktuell und belegt ist und kein offenes Finding sie berührt. Das letzte Tor: erst grün, dann offenlegen.
---

# Skill: Disclosure-Readiness (Berichtsreife-Gate)

Das **letzte Tor** vor der Offenlegung. Anders als die Objekt-Gates (Vollständigkeit *eines*
Objekts) prüft dieser Skill die **Release-Reife eines ganzen Themas**: Ist alles beisammen,
geprüft und unbestritten, um es im CSRD/ESRS-Bericht zu veröffentlichen?

## Die Prüfkette (alles muss grün sein)
| # | Kriterium | Quelle |
|---|-----------|--------|
| 1 | **Apparat vollständig** | `topic-gate` 100 % (IRO/Policy/Target/KPI/Maßnahme + alle wesentlichen IROs adressiert) |
| 2 | **Jeder Datenpunkt offengelegt** | jeder `datapoint` (`concerns: topic`) hat eine `disclosure` (`discloses`) |
| 3 | **Berichtete KPI aktuell** | jede `disclosure.reports`-KPI hat einen `kpi-value` fürs Berichtsjahr |
| 4 | **Belegt** | die KPI-Werte sind über `evidence` (`backs`) gestützt (→ `assurance`) |
| 5 | **Keine offenen Findings** | kein `finding` mit `status: offen`, das eine berichtete KPI `affects` |

## Ablauf
1. `python3 tools/query.py berichtsreife <topic-id>` → Verdikt **BERICHTSREIF / NICHT BERICHTSREIF** + Blocker-Liste.
2. Jeden Blocker schließen: fehlende Offenlegung schreiben, KPI-Wert nachtragen, Evidenz anhängen,
   offenes Finding über eine `remediation` schließen (→ `assurance`).
3. Erneut prüfen, bis das Verdikt grün ist.

## Harte Regeln
- ⛔ **Offenes Finding = nicht berichtsreif.** Solange ein offenes Finding eine berichtete KPI berührt, bleibt der Wert *vorläufig* — nicht offenlegen. (Genau hier verzahnt sich `assurance`.)
- 📎 **Keine Zahl ohne Beleg im Bericht.** Berichtete KPIs brauchen Evidenz; sonst ist die Offenlegung nicht prüfungssicher.
- 🚫 **Kein Datenpunkt ohne Offenlegung.** Eine ESRS-Pflicht ohne erfüllenden Berichtstext ist eine Compliance-Lücke.
- 🟢 **Das Gate ist binär.** Es gibt kein „zu 80 % berichtsreif" — entweder alle Blocker sind weg, oder es wird nicht freigegeben.

## Vor dem Abschluss
- [ ] `berichtsreife <topic>` zeigt ✅ BERICHTSREIF
- [ ] Alle berichteten KPIs: aktueller Wert + Evidenz, keine offenen Findings
- [ ] `validate.py` grün

> Sitzt am Ende der Kette: `iro-gate → policy-gate → target-gate → initiative-gate → kpi-gate`
> füllen den Apparat; `assurance` macht ihn prüfbar; **disclosure-readiness** gibt ihn frei.
