# Product Readiness — Sustainability OS als wiederverwendbares Template

> **Zweck dieses Dokuments.** Den Prototyp (entwickelt am Vaillant-Beispiel) in ein
> **einsetzbares Produkt** überführen: ein framework-agnostisches Template, das bei einem Kunden
> ausgerollt wird — startend mit *einem* Thema, in das der Kunde seine Governance,
> Verantwortlichkeiten, Policies, Ziele, KPIs und Maßnahmen pflegt; danach schrittweise erweitert.
>
> **Nicht-Ziel.** Der Vaillant-Graph muss weder inhaltlich vollständig noch konsistent sein. Er ist
> Gerüst. Perfektioniert wird das **Modell/Engine**, nicht die Instanz.

---

## 1. Produkt-Scope: framework-agnostisch

Der Kern bildet **Nachhaltigkeits-Governance generell** ab — nicht nur ESRS. Die universelle
Schleife ist:

```
  Bewerten (Wesentlichkeit) → Steuern (Policy · Ziel · Maßnahme)
       → Messen (KPI · Zeitreihe) → Prüfen (Assurance) → Offenlegen (Datenpunkt/Bericht)
```

ESRS ist die **erste Ausprägung**, nicht die Grundannahme. Andere Rahmenwerke (GRI, freiwillige
Programme, kundeneigene Governance) müssen als **Framework-Pack** andocken können, ohne den Kern
anzufassen.

## 2. Drei-Schichten-Architektur (der zentrale Schnitt)

| Schicht | Was | Ausgeliefert? | Beispiele (heute) |
|---|---|---|---|
| **A — Core Engine** *(framework-agnostisch)* | Objekt-Grammatik + Qualitäts-Gates + Validator + Abfrage/Index + Visualisierung **+ Wesentlichkeit (DMA/IRO) als Scope-Fundament** | **ja, als Produkt** | `object-schema.yaml`, `validate.py`, `query.py`, `linkage_guard.py`, Graph-Viz, generische Gates (target/kpi/policy/initiative/**iro/topic**, iro-coverage, assumption/risk/approval, performance-tracking, assurance) |
| **B — Framework-Pack** *(pluggable)* | Standard-spezifische **Offenlegung**: Referenz-Kataloge + Datenpunkt-Mapping + Bericht | **ja, je Pack** | **ESRS-Pack:** Kataloge, Konzept-Spines, Datenpunkt-/Disclosure-Schicht, `import_esrs_catalog.py`, `gen_datapoints.py`, `bericht_entwurf.py`, Anwendbarkeits-*Semantik* |
| **C — Kunden-Instanz** *(pro Deployment)* | Firmenkontext, Team, gewählte Pack(s) + Thema(en), die gepflegten Objekte | **nein, entsteht beim Kunden** | `objects/*.md`, `anwendbarkeit-*.yaml`, Roster/Company-Config, `reporting/*` |

**Wichtige Festlegung — DMA/IRO bleibt im Core, NICHT im Pack.** Die Wesentlichkeitsanalyse ist der
**Scope-Definierer**: Sie sagt, *wofür* überhaupt Policies, Ziele, KPIs und Maßnahmen gebraucht
werden. Ohne sie ist „ein Ziel anlegen" beliebig; mit ihr ist jedes Steuerungsobjekt an eine
wesentliche IRO verankert. Genau diese Verankerung ist die Stärke des Modells und gilt für *jedes*
Rahmenwerk (auch freiwillige). Standard-spezifisch ist nur, **welche Offenlegung** aus der
gesteuerten Wesentlichkeit folgt — und das ist Pack. Der Core kennt also: *Wesentlichkeit (IRO) →
Verantwortung, Ziel, Maßnahme, Kennzahl, Annahme, Risiko, Freigabe, Vollständigkeit.*

## 3. Template-/Instanz-Grenze (heute verschmolzen — Kinderkrankheit #0)

Alles steckt aktuell in `vaillant-dma-2026/`. Es gibt **keinen leeren Startpunkt**. Für ein Produkt:
- [ ] **Auslieferungs-Repo/Ordner** = Core (A) + Framework-Packs (B), ohne eine einzige Kundenzeile.
- [ ] **Kunden-Scaffold-Generator**: erzeugt eine leere Instanz (C) aus Parametern
      (Firmenname, Team-Roster, gewählte Packs, Thema(en) im Scope) — keine Vaillant-Kopie.
- [ ] **Company-Config als Daten**, nicht in CLAUDE.md hartcodiert (`instance-config.yaml`:
      Firma, Roster, Packs, Themen, Vertraulichkeits-Defaults).

## 4. Kinderkrankheiten-Liste (was „fertig" blockiert)

| # | Kinderkrankheit | Schicht | Warum kritisch fürs Produkt |
|---|---|---|---|
| 0 | Template & Instanz verschmolzen, kein leeres Scaffold | A/C | Ohne das kein Kunden-Rollout |
| 1 | Framework-Kopplung nicht abstrahiert (Core/Pack vermischt) | A/B | Voraussetzung für „über ESRS hinaus" |
| 2 | Kein geführter Onboarding-/Intake-Flow für ein Thema | A | Das ist die eigentliche Produkt-UX |
| 3 | Stille Owner-Zuweisung, kein RASCI/Handover | A | Governance ist das **Erste**, was der Kunde pflegt |
| 4 | Kein Dedup-Schutz | A | Mehr-Nutzer-Intake erzeugt sonst Dubletten |
| 5 | Kein Such-Index/Scope-Resolver | A | Usability für Nicht-Schema-Kenner + Token-Kosten |
| 6 | Datentyp-Klassifikation heuristisch | B (ESRS) | Erst bei Erweiterung Richtung Bericht relevant |
| 7 | Datenpunkt nicht versionsstabil | B (ESRS) | dito — Pack-Reife, nicht Tag-1 |

*(Die bestehenden TODO-Notizen `TODO-ownership-rasci`, `-suchlogik-navigation`, `-duplikate-vermeiden`,
`-esrs-datenpunkt-konzepte`, `-datentyp-review*` decken #3–#7 ab; #0–#2 sind neu.)*

## 5. Definition of Done (was „fertiges Produkt" heißt)

- [ ] Ein Operator setzt eine **neue Kunden-Instanz in wenigen Schritten** auf (Scaffold + Pack(s) + Thema), ohne Vaillant-Reste.
- [ ] Der Kunde pflegt für **ein Thema** Governance → Verantwortliche → Policy → Ziele → KPIs → Maßnahmen; die **Gates erzwingen Vollständigkeit**, nichts wird still durchgelassen.
- [ ] **Keine stille Verantwortung** (Handover bestätigt) und **keine Dubletten** (Dedup an der Anlage).
- [ ] **Navigation ohne Schema-Wissen** (NL → Scope → Antwort), ohne Full-Scan.
- [ ] **Erweiterbar**: zweites Thema / zweiter Pack ohne Core-Änderung.
- [ ] **Dokumentiert**: Operator-Setup-Guide + Kunden-Intake-Guide.

## 6. Empfohlene Reihenfolge

```
  Phase A — Fundament
     • Architektur-Schnitt Core/Pack/Instanz formal festlegen (Manifest je Pack)
     • leeres Kunden-Scaffold + instance-config.yaml
  Phase B — Governance-Engine (Tag-1-Intake sauber)
     • RASCI-Rollen + Handover in Schema/Validator/Gates
     • Dedup-Check als Gate-Schritt-0
  Phase C — Onboarding-Flow
     • geführter Intake für EIN Thema (Skill), Gates verdrahtet
  Phase D — Usability
     • Such-Index + Scope-Resolver (NL → Anker)
  Phase E — Reporting-Pack-Reife (bei Bedarf der Erweiterung)
     • Datentyp-Review-Mechanik, Datenpunkt-Konzepte (Versionsstabilität)
  Phase F — Agnostik beweisen
     • zweiten Framework-Pack (z. B. freiwilliges Programm) andocken
```

## 7. Offene Produkt-Entscheidungen
- **Pack-Granularität:** ein ESRS-Pack gesamt, oder je Standard ein Sub-Pack (E1, S1, …)?
- **Multi-Tenancy:** eine Instanz = ein Kunde (ein Repo) — oder mehrere Kunden in einem Mandantenmodell?
- **Intake-Kanal:** rein über Skills/Chat, oder zusätzlich ein einfaches Formular/Import (CSV) für Bulk-Pflege?
- **Wesentlichkeit optional:** Core ohne DMA nutzbar machen (freiwillige Programme), DMA nur im ESRS-Pack?
- **Versionierung des Templates:** wie bekommen bestehende Kunden-Instanzen Engine-/Pack-Updates?

---

### Verwandte Notizen auf dem Branch
`TODO-ownership-rasci.md` · `TODO-suchlogik-navigation.md` · `TODO-duplikate-vermeiden.md` ·
`TODO-esrs-datenpunkt-konzepte.md` · `TODO-datentyp-review` · `SALES-ARGUMENTE.md`
