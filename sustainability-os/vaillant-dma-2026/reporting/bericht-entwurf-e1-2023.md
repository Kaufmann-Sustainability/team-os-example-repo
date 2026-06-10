# Berichts-Entwurf — ESRS E1  ·  Fassung `esrs-2023`

> **MASCHINENGENERIERTER ROH-ENTWURF — nicht freigegeben.** Erzeugt 2026-06-10 via `tools/bericht_entwurf.py --version 2023`. Kunde: `vaillant-dma-2026`.
>
> Inhalt ist über **stabile Konzepte** zugeordnet (versionsunabhängig); diese Fassung nummeriert sie als `esrs-2023`. Quellen sind als **(manuell)** [autoritativ] oder **(abgeleitet)** [Tier-1-Regel, deterministisch] markiert. Inhaltliche Vollständigkeit je Absatz ist im Review zu prüfen.

**Stand:** 8 anwendbare DRs · 4 mit Inhalt · 4 offen · 1 ausgeschlossen.


---

## E1-1 — Transition plan for climate change mitigation  ·  ⚠ OFFEN — kein Inhalt zugeordnet

*Konzept:* `transition-plan`  ·  *anwendbar, weil:* Klimaschutz wesentlich -> Transitionsplan verpflichtend


**E1-1 ¶14**  _(narrativ)_
> Die Angaben zum Transitionsplan für den Klimaschutz umfassen Reduktionsziele, Dekarbonisierungshebel, Schlüsselmaßnahmen und Investitionen.

⚠ **OFFEN** — kein Inhalt für Konzept `transition-plan` zugeordnet.

**E1-1 ¶16(g)**  _(narrativ)_
> Erläuterung, wie der Transitionsplan in die allgemeine Geschäftsstrategie und Finanzplanung eingebettet ist.

⚠ **OFFEN** — kein Inhalt für Konzept `transition-plan` zugeordnet.

---

## E1-2 — Policies related to climate change mitigation and adaptation  ·  ✅ Inhalt zugeordnet

*Konzept:* `policies-climate`  ·  *anwendbar, weil:* Policy zu Klimaschutz/Anpassung wesentlich

**Quellen (abgeleitet · Tier-1-Regel):**
- `policy-e1-energie` — Policy: Energiemanagement-Policy (ISO 50001)  _(type=policy ∧ concerns->topic-e1-*)_
- `policy-e1-klimaschutz-transitionsplan` — Policy: Klimaschutz- & Transitionsplan (ESRS E1-1)  _(type=policy ∧ concerns->topic-e1-*)_
- `policy-e1-klimawandel-adaptation` — Policy: Klimaanpassungs-Richtlinie  _(type=policy ∧ concerns->topic-e1-*)_
- `policy-e1-nachhaltige-beschaffung` — Policy: Nachhaltige Beschaffung & Vorkette (ESRS E1-1)  _(type=policy ∧ concerns->topic-e1-*)_


**E1-2 ¶24**  _(narrativ)_
> Das Unternehmen legt die Konzepte (Policies) zur Steuerung seiner wesentlichen Auswirkungen, Risiken und Chancen in Bezug auf Klimaschutz und -anpassung offen.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

**E1-2 ¶25**  _(narrativ)_
> Verweis auf ESRS 2 MDR-P; Angabe, ob die Policies Klimaschutz, -anpassung, Energieeffizienz, erneuerbare Energie u. a. adressieren.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

---

## E1-3 — Actions and resources in relation to climate change policies  ·  ✅ Inhalt zugeordnet

*Konzept:* `actions-climate`  ·  *anwendbar, weil:* Maßnahmen/Ressourcen wesentlich

**Quellen (abgeleitet · Tier-1-Regel):**
- `initiative-e1-energie` — Initiative: Effizienzprogramm Werke  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-gasausstieg-portfolio` — Maßnahme: Gasausstieg & Hybrid-Portfolioumbau  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-gruene-beschaffung` — Maßnahme: Grüne Materialbeschaffung  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-installateurs-qualifizierung` — Maßnahme: Installateurs-Qualifizierung (Academy)  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-klimawandel-adaptation` — Initiative: Resilienz-Programm Produktionsstandorte  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-logistik-dekarb` — Maßnahme: Logistik-Dekarbonisierung  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-scope12-netzero` — Maßnahme: Scope 1+2 Net-Zero (Prozesswärme-Elektrifizierung)  _(type=initiative ∧ supports->target-e1-*)_
- `initiative-e1-waermepumpen-hochlauf` — Maßnahme: Wärmepumpen-Kapazitätshochlauf (Senica)  _(type=initiative ∧ supports->target-e1-*)_


**E1-3 ¶29**  _(narrativ)_
> Das Unternehmen legt seine Klimaschutz-Maßnahmen und die zugewiesenen Ressourcen offen (Verweis ESRS 2 MDR-A).

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

**E1-3 ¶29(a)**  _(narrativ)_
> Zuordnung der wichtigsten Maßnahmen zu Dekarbonisierungshebeln und erwartete THG-Reduktion.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

---

## E1-4 — Targets related to climate change mitigation and adaptation  ·  ✅ Inhalt zugeordnet

*Konzept:* `targets-climate`  ·  *anwendbar, weil:* THG-Reduktionsziele gesetzt

**Quellen (manuell · `satisfied_by`):**
- `target-e1-scope1-2-netzero` — Ziel: Scope 1+2 Net-Zero bis 2030 (37.965 → 0 tCO₂e)
- `target-e1-scope3-1-embodied` — Ziel: Eingebetteter Kohlenstoff je Einheit −30 % bis 2032 (Index 100 → 70)
- `target-e1-scope3-11-usephase` — Ziel: Use-Phase-Emissionen (Scope 3.11) 133 → 60 Mt CO₂e bis 2035
- `target-e1-scope3-logistik` — Ziel: Logistik-Emissionen (Scope 3.4/3.9) −25 % bis 2030

**Quellen (abgeleitet · Tier-1-Regel):**
- `target-e1-scope1-2-netzero` — Ziel: Scope 1+2 Net-Zero bis 2030 (37.965 → 0 tCO₂e)  _(type=target ∧ addresses->iro-e1-*)_
- `target-e1-scope3-1-embodied` — Ziel: Eingebetteter Kohlenstoff je Einheit −30 % bis 2032 (Index 100 → 70)  _(type=target ∧ addresses->iro-e1-*)_
- `target-e1-scope3-11-usephase` — Ziel: Use-Phase-Emissionen (Scope 3.11) 133 → 60 Mt CO₂e bis 2035  _(type=target ∧ addresses->iro-e1-*)_
- `target-e1-scope3-logistik` — Ziel: Logistik-Emissionen (Scope 3.4/3.9) −25 % bis 2030  _(type=target ∧ addresses->iro-e1-*)_
- `target-e1-waermepumpen-absatzanteil` — Ziel: Wärmepumpen-Absatzanteil 40 % → 80 % bis 2030  _(type=target ∧ addresses->iro-e1-*)_


**E1-4 ¶34**  _(narrativ)_
> Das Unternehmen legt die im Zusammenhang mit Klimaschutz und -anpassung gesetzten Ziele offen.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

**E1-4 ¶34(a)**  _(quantitativ)_
> Absolute oder intensitätsbezogene THG-Reduktionsziele für Scope 1, 2 und 3.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

**E1-4 ¶34(c)**  _(narrativ)_
> Angabe, ob die Ziele wissenschaftsbasiert und mit der Begrenzung der Erderwärmung auf 1,5 °C vereinbar sind.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

---

## E1-5 — Energy consumption and mix  ·  ⚠ OFFEN — kein Inhalt zugeordnet

*Konzept:* `energy`  ·  *anwendbar, weil:* Energieverbrauch wesentlich (topic-e1-energie)


**E1-5 ¶37**  _(quantitativ)_
> Gesamtenergieverbrauch in MWh, aufgeschlüsselt nach fossilen, nuklearen und erneuerbaren Quellen.

⚠ **OFFEN** — kein Inhalt für Konzept `energy` zugeordnet.

**E1-5 ¶38**  _(quantitativ)_
> Energieintensität je Nettoumsatz (MWh pro Geldeinheit) für Tätigkeiten in klimaintensiven Sektoren.

⚠ **OFFEN** — kein Inhalt für Konzept `energy` zugeordnet.

---

## E1-6 — Gross Scopes 1, 2, 3 and Total GHG emissions  ·  ✅ Inhalt zugeordnet

*Konzept:* `gross-ghg`  ·  *anwendbar, weil:* Brutto-THG-Emissionen wesentlich

**Quellen (manuell · `satisfied_by`):**
- `kpi-e1-scope1-2` — KPI: Scope 1+2 absolut
- `kpi-e1-scope3-11` — KPI: Scope-3.11 Nutzungsphasen-Emissionen


**E1-6 ¶44**  _(quantitativ)_
> Brutto-Scope-1-, Scope-2- und Scope-3-THG-Emissionen sowie Gesamt-THG-Emissionen in tCO2e.

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

**E1-6 ¶48**  _(quantitativ)_
> THG-Intensität (Gesamtemissionen je Nettoumsatz).

_Entwurf:_ aus o. g. Quelle(n) zu verfassen — **Absatz-Abdeckung im Review prüfen.**

---

## E1-7 — GHG removals and GHG mitigation projects financed through carbon credits  ·  ⚠ OFFEN — kein Inhalt zugeordnet

*Konzept:* `removals-credits`  ·  *anwendbar, weil:* Removals/Carbon-Credits genutzt


**E1-7 ¶56**  _(quantitativ)_
> THG-Entnahmen und -Speicherung in der eigenen Wertschöpfungskette in tCO2e.

⚠ **OFFEN** — kein Inhalt für Konzept `removals-credits` zugeordnet.

---

## E1-9 — Anticipated financial effects from material physical and transition risks  ·  ⚠ OFFEN — kein Inhalt zugeordnet

*Konzept:* `financial-effects`  ·  *anwendbar, weil:* Wesentliche physische & transitorische Risiken -> finanzielle Effekte


**E1-9 ¶67**  _(quantitativ)_
> Erwartete finanzielle Effekte aus wesentlichen physischen und transitorischen Klimarisiken.

⚠ **OFFEN** — kein Inhalt für Konzept `financial-effects` zugeordnet.

---

## Nicht anwendbar (Ausschlüsse — prüfungsrelevant)
- **E1-8** (internal-carbon-price) — Kein internes CO2-Bepreisungsschema im Einsatz (¶37 bedingt anwendbar)
