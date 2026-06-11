---
name: iro-gate
description: Vollständigkeits-Wächter für IROs (Impacts/Risks/Opportunities der Wesentlichkeitsanalyse). Einsetzen, wenn eine IRO angelegt oder bewertet wird — erzwingt den TYP-abhängigen Score (Impact → Impact-Bewertung, Risk/Opportunity → Financial-Bewertung), Wertschöpfungsketten-Position, Begründung und — wenn wesentlich — den Steuerungs-Anschluss. Keine IRO ohne nachvollziehbare Bewertung.
---

# Skill: IRO-Gate (Vollständigkeits-Vertrag für IROs)

Eine IRO ist das Kernobjekt der doppelten Wesentlichkeit. Sie ist erst *belastbar*, wenn klar ist:
welcher Typ, wo in der Wertschöpfungskette, warum so bewertet — und, wenn wesentlich, dass sie
auch gesteuert wird. Dieser Skill ist der **Wächter**.

## Die eine Regel, die zählt: Score nach Typ
> **Impact (I)** → nur die **Impact-Bewertung** ist nötig (Ausmaß, Umfang, ggf. Unabwendbarkeit;
> plus *tatsächlich* vs. *potenziell*).
> **Risk / Opportunity (R/O)** → nur die **Financial-Bewertung** ist nötig (finanzieller Effekt × Eintrittswahrscheinlichkeit).
>
> Ein Impact braucht keinen Financial-Score, eine R/O keinen Impact-Score. Beides erzwingen wäre
> Scheingenauigkeit — das Schema verlangt es daher **nicht**; dieses Gate verlangt das jeweils Richtige.

## Der Vertrag (Kern-Pflichten)
| # | Pflicht | Feld |
|---|---------|------|
| 1 | **Typ + Wesentlichkeit** | `iro_typ` (Impact-positiv/-negativ \| Risk \| Opportunity) + `wesentlich` (ja/nein) |
| 2 | **Wertschöpfungsketten-Position** | `wertschoepfungskette: upstream \| eigene-ops \| downstream` |
| 3 | **Begründung** | `begruendung:` — *warum* diese Bewertung? (nicht im Fließtext verstecken) |
| 4a | **wenn Impact** | `impact_wesentlichkeit` **+** `wirkung_art: tatsächlich \| potenziell` |
| 4b | **wenn Risk/Opportunity** | `finanz_wesentlichkeit` |
| 5 | **wenn `wesentlich: ja`** | mind. ein `target` mit `addresses: [diese IRO]` (→ `iro-coverage`) |
| 6 | **Kurztitel** (empfohlen) | `kurztitel:` — 3–6 Wörter, menschlich; das Label, das Views (Cockpit/Offenlegung) zeigen |

## Guter `kurztitel` (das menschliche Label)
Der H1-Titel ist oft generisch (`IRO E1-I1: Klimawandel-Mitigation`) und `iro_nr` (`E1-I1`)
ist kryptisch — Views brauchen einen **kurzen, sprechenden Griff**. Den setzt du hier, einmal,
beim Bewerten. Regeln: **3–6 Wörter**, der *Kern* (Quelle/Mechanismus), kein ganzer Satz,
kein nacktes Standard-Kürzel.

| statt | `kurztitel` |
|-------|-------------|
| „IRO E1-I1: Klimawandel-Mitigation" | **Gaskessel-Bestand: fossiler Lock-in** |
| „IRO E1-I2: Klimawandel-Mitigation" | **Eigenbetrieb Scope 1+2** |
| „IRO E1-I5: Klimawandel-Mitigation" | **Wärmepumpen vermeiden Kundenemissionen** |

Fehlt `kurztitel`, fallen Views auf `iro_nr` zurück — es bricht nichts, aber die Oberfläche
bleibt kryptisch. Darum: **bei jeder IRO setzen.**

## Ablauf
1. `python3 tools/query.py reifegrad <iro-id>` (oder `<topic-id>` für alle IROs des Themas).
2. Fehlende Felder ergänzen — typgerecht (Score nicht doppeln).
3. Wenn wesentlich, aber unadressiert → `iro-coverage` ziehen (Ziel/Policy verlinken) oder als `offene_punkte` markieren.

## Harte Regeln
- 🚫 **Keine IRO ohne Begründung und Wertschöpfungsketten-Position** — sonst ist die Bewertung nicht prüfbar.
- 🎯 **Score typgerecht.** Impact ohne Impact-Score = unbewertet; R/O ohne Financial-Score = unbewertet. Den jeweils *anderen* Score nicht erfinden.
- 🔗 **Wesentlich heißt gesteuert.** `wesentlich: ja` ohne adressierendes Ziel ist eine Lücke → markieren.
- 🧪 IRO `scored_under` eine dokumentierte `methodology` (Governance-Spur).

## Vor dem Abschluss
- [ ] `reifegrad <iro>` 100 % **oder** jede offene Pflicht in `offene_punkte`
- [ ] Score entspricht dem Typ (kein doppelter Score)
- [ ] `kurztitel` gesetzt (3–6 Wörter, sprechend)
- [ ] `validate.py` grün
