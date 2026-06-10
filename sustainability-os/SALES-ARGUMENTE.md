# Sales-Argumente — Sustainability OS

> Ein Nachhaltigkeits-OS, das die ganze CSRD/ESRS-Steuerung als **verknüpften Objekt-Graph**
> abbildet — nicht als Dokumente in Ordnern. Jedes Ziel, jede IRO, jede Kennzahl, jede
> Offenlegung ist ein Objekt mit geprüften Beziehungen, versioniert in Git, durchgesetzt von
> Skills, die Qualität *erzwingen*. Alle Funktionen unten sind an einem echten ESRS-E1-Beispiel
> (Vaillant) demonstriert, validiert und im Graph sichtbar.

---

## 1. Map once, report many — eine Wahrheit, n Sichten ⭐
**Der Schmerz:** Jedes Framework und jedes Rating — ESRS, CDP, EcoVadis, GRI, ISSB, MSCI — fragt
größtenteils *dasselbe* in anderer Verpackung. Teams beantworten die Scope-1-Frage fünfmal, in
fünf Tools, mit fünf leicht abweichenden Zahlen. Inkonsistenz ist vorprogrammiert, und jeder neue
Fragebogen ist Arbeit von vorn.

**Was das OS tut:** Der **Inhalt ist kanonisch** — ein Scope-1-Wert, eine Policy, ein Target
existieren *einmal* als Objekt. Eine Berichtsanforderung ist nur ein Knoten mit `framework`-Feld,
der per Kante auf den füllenden Inhalt zeigt. Der Crosswalk zwischen Frameworks wird zu
**Graph-Kanten** (`equivalent_to` / `satisfied_by`), nicht zu einer gepflegten Mapping-Tabelle.

**Der Effekt:** ESRS E1-6, CDP C6 und ISSB S2 zeigen alle auf denselben Wert. Ein **neues Rating =
Kanten ziehen, kein neuer Inhalt**. Inkonsistenz zwischen Frameworks wird strukturell unmöglich.
Aus „wir füllen den fünften Fragebogen" wird „wir berichten eine Wahrheit in fünf Sichten".

---

## 2. Reifegrad auf Knopfdruck — „sind wir vollständig?" in Sekunden
**Der Schmerz:** Die Frage „ist dieses Thema steuerungs- und berichtsbereit?" kostet heute eine
wochenlange manuelle Bestandsaufnahme über verstreute Decks, Sheets und Mailverläufe.

**Was das OS tut:** Jeder Objekttyp hat einen **Vollständigkeits-Vertrag** (Wächter-Skills). Ein
Befehl scort jedes Ziel, jede Maßnahme, jede IRO, jede KPI und das Thema selbst gegen seinen
Vertrag und zeigt **exakt, was fehlt** — als Dashboard mit Reifegrad-Balken.

**Der Effekt:** „Ziel zu 62 % — es fehlen Annahme, Freigabe und Risikobewertung." Lücken werden
**markiert, nie still weggelassen** (`offene_punkte`). Aus einem Audit-Marathon wird ein
Knopfdruck. Qualität kommt rein, nicht raus.

---

## 3. Das Berichts-Veto — prüfungssicher by design
**Der Schmerz:** Zahlen wandern in den Geschäftsbericht, deren Datenqualität intern noch strittig
ist. Auffallen tut es — wenn überhaupt — beim Wirtschaftsprüfer.

**Was das OS tut:** Ein binäres **Release-Gate** prüft vor der Offenlegung: steht der Apparat, ist
jeder Datenpunkt offengelegt, ist jede berichtete Kennzahl aktuell und belegt — und berührt sie
**kein offenes Finding**?

**Der Effekt:** Im Beispiel **blockierte das Gate automatisch die E1-6-Offenlegung**, weil ein
offenes Datenqualitäts-Finding die berichtete Scope-3.11-Kennzahl berührte. Eine unbelegbare Zahl
kommt gar nicht erst in den Bericht. Prüfungssicherheit ist nicht mehr Hoffnung, sondern Regel.

---

## 4. Off-track, bevor es zu spät ist
**Der Schmerz:** Dass ein Ziel den Pfad verfehlt, merkt man oft erst im Jahresbericht — wenn zum
Gegensteuern keine Zeit mehr ist.

**Was das OS tut:** Kennzahlen sind eine **lebende Zeitreihe** (Ist-Wert je Jahr + Forecast +
Trend). Ein Befehl zeigt je KPI: aktueller Stand, Projektion, on-/off-track — und **Datenlücken**.

**Der Effekt:** Das System meldete von selbst: **Scope 3.11 off-track** (Forecast verfehlt das
Ziel) und **vier Kennzahlen ohne Ist-Werte**. Abweichung wird zum Frühwarnsignal statt zur
Jahresend-Überraschung.

---

## 5. „Worauf beruht das?" — eine Ein-Hop-Frage
**Der Schmerz:** Die Annahmen hinter Zielen leben in Köpfen und alten Slides. Ändert sich die
Förderlage, weiß niemand mehr, welche Ziele daran hingen.

**Was das OS tut:** Jede tragende Annahme ist ein Objekt mit **Confidence + Quelle**, verknüpft
mit dem Ziel/der Entscheidung, das darauf ruht. Provenienz ist erstklassig, nicht im Fließtext
vergraben.

**Der Effekt:** Eine **niedrig-Confidence-Annahme** („Förderung bleibt stabil") hängt sichtbar
unter dem Absatzziel — verkettet mit dem zugehörigen Risiko und einer Hedge-Empfehlung. „Welche
Ziele wackeln, wenn diese Annahme kippt?" ist eine Abfrage, keine Archäologie.

---

## 6. Doppelte Wesentlichkeit, lückenlos
**Der Schmerz:** Eine als wesentlich bewertete IRO ohne Steuerung ist ein Compliance-Loch — und
unter 120 wesentlichen IROs von Hand kaum zu finden.

**Was das OS tut:** Jede wesentliche IRO **muss** durch Strategie, Policy oder Ziel adressiert
sein. Der Score ist typgerecht: Impacts über die Impact-Bewertung, Risiken/Chancen über die
finanzielle — keine Scheingenauigkeit.

**Der Effekt:** Das System findet die *eine* unadressierte Risiko-IRO unter hunderten. Die Brücke
von „bewertet" zu „gesteuert" wird erzwungen, nicht gehofft.

---

## 7. Prüfspur eingebaut
**Der Schmerz:** Der Auditor fragt „beweisen Sie mir Zahl X" — und das Team sucht tagelang nach
Herleitung, Kontrolle und Nachweis.

**Was das OS tut:** Jede berichtsrelevante Kennzahl trägt eine Kette: **Kontrolle → Test →
Nachweis → Finding → Behebung**. Die Spur „Zahl → Quelle → Kontrolle → Offenlegung" ist lückenlos
im Graph.

**Der Effekt:** Assurance ist kein Jahresend-Feuerlöschen mehr, sondern ein Zustand, den man jederzeit
abfragt.

---

## 8. Das Wissen steckt im System, nicht in zwei Köpfen
**Der Schmerz:** Berichtsqualität hängt an ein, zwei Expert:innen. Neue Teammitglieder — oder
Zulieferer aus HR und Einkauf — brauchen Monate, bis sie „es richtig machen".

**Was das OS tut:** **Skills** führen jeden durch die korrekte Erstellung jedes Objekts —
Vollständigkeit, Konsistenz, Verknüpfung. Das Regelwerk ist Teil des Systems, nicht des Flurfunks.

**Der Effekt:** Auch Nicht-Expert:innen legen OS-konforme, prüfbare Objekte an. Onboarding in
Tagen statt Monaten. Das Wissen bleibt, auch wenn Menschen gehen.

---

## 9. Kein Lock-in, alles nachvollziehbar
**Der Schmerz:** Daten gefangen in einem proprietären Tool. Keine echte Historie, kein „wer hat
was wann und warum geändert", kein sauberer Export.

**Was das OS tut:** Jedes Objekt ist **Klartext (Markdown), versioniert in Git**, geprüft von
einem Validator. Der gesamte Nachhaltigkeitszustand des Konzerns ist ein navigierbarer,
visualisierbarer Graph.

**Der Effekt:** Jede Änderung ist auditierbar und umkehrbar. Kein Anbieter-Lock-in. Der „Bericht"
ist kein PDF am Jahresende, sondern ein jederzeit abfragbarer Live-Zustand.

---

## 10. Ergänzt eure Software, ersetzt sie nicht
**Der Schmerz:** „Müssen wir unsere Datenplattform rauswerfen?" — die Angst vor dem Rip-and-replace.

**Was das OS tut:** Zwei Ebenen mit klarer Grenze. Die **Roh- und Standortdaten bleiben in eurer
Software** (System of Record). Das OS sitzt darüber als **Governance- und Bedeutungsschicht** und
verlinkt per Referenz (`sourced_from`) — es dupliziert keine 48.000 Messwerte.

**Der Effekt:** Sofort einführbar neben dem Bestand. Eure Datenplattform liefert die Zahlen, das
OS liefert Steuerung, Prüfspur und Berichtsreife darüber.

---

### Der rote Faden
Alles oben ist **ein** Objektmodell: Bewertung (IRO) → Steuerung (Policy, Target, Maßnahme) →
Messung (KPI, Zeitreihe) → Prüfung (Assurance) → Offenlegung (Datenpunkt, Disclosure) → und quer
darüber jedes externe Framework als Sicht. Eine Wahrheit, durchgängig verknüpft, von Skills
sauber gehalten — **map once, govern continuously, report many.**
