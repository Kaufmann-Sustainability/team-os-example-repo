# TODO — ESRS-Datenpunkte als Konzepte definieren

> **Ziel:** Einzelne ESRS-Datenpunkte versions­stabil verankern — so wie heute schon die
> **DRs** über `reference/esrs-concepts.yaml` an stabile Konzepte gebunden sind, nicht an
> DR-Codes. Eine Ebene tiefer fehlt das noch.

## Warum (das Problem)

Heute hängt ein Datenpunkt-Objekt an einem **versions­spezifischen String**:

```yaml
# objects/datapoint-ecdraft2026-e1-8-30ai.md
esrs_datapoint: "E1-8 ¶30(a)i."   # ⚠ gilt NUR für ec-draft-2026
concept: gross-ghg                 # stabil (DR-Ebene), aber zu grob für den einzelnen Punkt
```

Das `¶30(a)i.` ändert sich zwischen Katalog-Fassungen (ESRS-2023 ↔ EC-Entwurf-2026 nummerieren
Absätze um). Damit ist die Datenpunkt-Identität **brüchig** — exakt das Problem, das Konzepte auf
DR-Ebene gelöst haben (`map once, report many`), nur noch ungelöst auf Datenpunkt-Ebene.

## Zielmodell

Jeder *echte* (reviewte, quantitative) Datenpunkt bekommt ein **stabiles Konzept** mit einer
`nummerierung` je Katalog-Version — analog zur DR-Spine:

```yaml
# reference/esrs-datapoint-concepts-e1.yaml  (NEU)
- id: dp-ghg-scope1
  name: "Scope-1-THG-Emissionen (absolut)"
  parent: gross-ghg            # DR-Konzept (bestehende Spine)
  einheit: "tCO₂eq"
  nummerierung:
    esrs-2023:      "E1-6 ¶44(a)"
    ec-draft-2026:  "E1-8 ¶30(a)i."
```

Das Datenpunkt-Objekt ankert dann an `dp-ghg-scope1` (stabil); der Absatz-Verweis je Fassung wird
aus der Spine **aufgelöst**, nicht im Objekt eingefroren. Folge: dieselben Objekte speisen den
E1-Bericht in **2023 UND ec-draft** — Abdeckung trägt über Versionen, genau wie bei DR-Konzepten.

---

## Arbeitsschritte

### 1. Scope & Granularität festlegen
- [ ] Nur als `quantitativ` **reviewte** Datenpunkte werden Konzepte
      (Input: `reference/datentyp-review-vaillant-e1.yaml` — die ~25 nach Freigabe).
- [ ] `container` / `narrativ` / `rahmen` bekommen **kein** Datenpunkt-Konzept (bleiben DR-Ebene).
- [ ] Entscheiden: gehören Aufschlüsselungs-Eltern (z. B. ¶26 „total energy") als eigener
      Aggregat-Datenpunkt dazu, oder nur die Blätter (a/b/c)?

### 2. Namenskonvention für stabile IDs
- [ ] Schema `dp-<thema>-<merkmal>` festlegen, menschenlesbar & versionsfrei.
      Beispiele: `dp-energy-fossil`, `dp-energy-renewable`, `dp-ghg-scope1`,
      `dp-ghg-scope2-locationbased`, `dp-ghg-scope2-marketbased`, `dp-ghg-scope3`.
- [ ] Kollisionsfreiheit & Stabilitäts-Regel dokumentieren (ID ändert sich nie, auch wenn
      ESRS umnummeriert).

### 3. Spine-Struktur anlegen
- [ ] `reference/esrs-datapoint-concepts-e1.yaml` mit Feldern:
      `id, name, parent (DR-Konzept), einheit, nummerierung{version→verweis}`.
- [ ] Klären: eigene Datei je Standard (wie `esrs-concepts-s1.yaml`) oder Sub-Block in der
      bestehenden Konzept-Spine.

### 4. Mapping befüllen (der eigentliche Inhalt)
- [ ] `ec-draft-2026`-Verweise übernehmen (liegen vor, aus dem Katalog).
- [ ] `esrs-2023`-Verweise gegenmappen — **Crosswalk** zwischen den Fassungen
      (teilweise n:1 oder „in 2023 nicht vorhanden" → `null`, wie `climate-risks` heute).
- [ ] Einheit/Methodik je Datenpunkt-Konzept ergänzen, wo sinnvoll.

### 5. Datenpunkt-Objekte migrieren
- [ ] Anker-Feld umstellen: statt String `esrs_datapoint` → stabile `datapoint_concept`-Kante.
- [ ] `esrs_datapoint` (Absatz-Verweis) nur noch **abgeleitet** anzeigen, aus der Spine je Version.
- [ ] ~20 declassed Objekte (Container/narrativ) gemäß Review zurückziehen.

### 6. Tooling anpassen
- [ ] `tools/validate.py`: neue Regel — `datapoint_concept` muss auf ein existierendes
      Datenpunkt-Konzept zeigen (referenzielle Integrität, wie bei `owner`).
- [ ] `tools/gen_datapoints.py`: Objekte je **Datenpunkt-Konzept** minten/refreshen
      (Idempotenz über die stabile ID, nicht über den Verweis-String).
- [ ] `tools/bericht_entwurf.py`: Abdeckung je Datenpunkt-Konzept → Verweis der **aktuellen**
      Version auflösen (versionsunabhängig, wie DR-Konzepte heute).
- [ ] `tools/import_esrs_catalog.py`: optional die Datenpunkt-Konzept-ID je Absatz mit-emittieren.

### 7. Beweis: Versionsunabhängigkeit
- [ ] E1-Bericht aus **denselben** Objekten für `2023` UND `ecdraft2026` erzeugen; prüfen, dass
      die Datenpunkt-Abdeckung in beiden Fassungen korrekt erscheint (der eigentliche Payoff).

### 8. Aufräumen & Konsistenz
- [ ] Rollup-Datenpunkt `datapoint-ecdraft-e1-8-thg` + CDP-`equivalent_to` mit der neuen
      Granularität abgleichen (Doppelmodellierung auflösen).
- [ ] `SALES-ARGUMENTE.md` #1/#11 nachziehen: „map once, report many" gilt jetzt bis auf
      Datenpunkt-Ebene.

### 9. Ausrollen
- [ ] Muster auf S1 (und weitere Standards) übertragen, sobald deren quantitative Datenpunkte
      reviewt sind.

---

## Offene Entscheidungen
- **Aggregat vs. Blatt:** Wird „total energy consumption" (¶26) ein eigenes Datenpunkt-Konzept
  oder nur die Summe seiner Blätter?
- **2023-Crosswalk-Tiefe:** Voll mappen oder nur dort, wo ein 2023-Äquivalent eindeutig ist?
- **Einheiten-Quelle:** Einheit am Datenpunkt-Konzept (Spine) oder weiter an der speisenden KPI?

## Bezug zum Bestehenden
- DR-Spine & `nummerierung`-Muster: `reference/esrs-concepts.yaml` (Vorbild 1:1 eine Ebene höher).
- Review-Input: `reference/datentyp-review-vaillant-e1.yaml`.
- Erzeuger/Konsumenten: `tools/{import_esrs_catalog,gen_datapoints,bericht_entwurf,validate}.py`.
