# TODO — Bestehenden Kundenbericht einlesen (Report → versionierte disclosure-Objekte)

> **Auslöser.** Ein Kunde, der **schon nach ESRS berichtet hat**, hat fertige Textblöcke je
> Offenlegungspflicht. Die sollen als Objekte ins OS — damit man im Folgejahr **nicht bei null**
> anfängt, sondern den Vorjahrestext fortschreibt und versioniert.

> **Gute Nachricht: der Typ existiert schon.** „Textblock je ESRS-Datenpunkt, je Berichtsjahr,
> versioniert" ist exakt `type: disclosure`:
> ```yaml
> disclosure:
>   pflichtfelder: [esrs_datapoint, berichtsjahr, version]
>   beziehungen:   [discloses, reports]   # discloses→datapoint, reports→kpi
> ```
> Es fehlt **kein Schema**, sondern **Prozess + Werkzeug**.

## Arbeitsschritte

### 1. Ingest-Werkzeug (Report → Objekte)
- [ ] `tools/import_report.py`: liest den bestehenden Bericht (Text/Markdown; PDF/DOCX → Text vorab).
- [ ] Segmentieren je **DR/Datenpunkt** und Textblock dem `esrs_datapoint` (Verweis) zuordnen —
      gegen den vorhandenen Katalog (`reference/esrs-catalog-*.yaml`).
- [ ] Je Block ein `disclosure`-Objekt erzeugen: `esrs_datapoint`, `berichtsjahr` (= Vorjahr),
      `version: 1`, Text im Body, `discloses: [datapoint-…]`, `reports: [kpi-…]` wo quantitativ.

### 2. Mapping-Review (menschlich, wie beim Datentyp-Review)
- [ ] Bestehende Berichte folgen nicht immer 1:1 der Datenpunkt-Granularität (Narrativ spannt
      mehrere ¶). Vorschlag automatisch, **Bestätigung durch den Menschen** — Fehlmapping ist teuer.
- [ ] Nicht zuordenbare Blöcke markieren statt still verwerfen.

### 3. Jahres-Übertrag / Versionierung (der eigentliche Nutzen)
- [ ] `carry_forward`: Vorjahres-`disclosure`s als **Entwurf** ins neue `berichtsjahr` kopieren,
      `version` hochzählen, Owner/Status zurücksetzen.
- [ ] **Veraltungs-Flag**: wenn die speisende `kpi` (über `reports`) einen neuen Wert hat oder ein
      offenes `finding` sie berührt → Disclosure „Text prüfen". Koppelt an `disclosure-readiness`.

### 4. Kreis schließen mit dem Generator
- [ ] `bericht_entwurf.py` erzeugt heute den Entwurf **aus** den Objekten; `import_report.py` ist die
      **Gegenrichtung** (Objekte aus einem Bericht). Zusammen: Erstbefüllung aus Altbericht →
      danach gepflegt im Graphen → Folgejahr per Generator + Carry-Forward.

## Nutzen
- **Onboarding eines Bestandskunden** in Stunden statt Wochen (vorhandener Bericht = Startkapital).
- **Kein Bei-null-Start** im Folgejahr: nur Deltas pflegen, Rest fortgeschrieben.
- Jeder Textblock wird **prüfbar verankert** (welcher Datenpunkt, welche KPI, welches Jahr, welche Version).

## Bezug zum Bestehenden
- Typ `disclosure` (existiert, 1 Instanz: `disclosure-e1-6-2025`).
- Katalog `reference/esrs-catalog-*.yaml` (Datenpunkt-Verweise fürs Mapping).
- Generator-Gegenstück `tools/bericht_entwurf.py`; Release-Gate `disclosure-readiness`.
