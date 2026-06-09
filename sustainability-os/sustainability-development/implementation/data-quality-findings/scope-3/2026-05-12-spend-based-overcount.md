# Datenqualitäts-Finding: Doppelzählung bei spend-based Scope-3-Kat.-1

**Datum:** 2026-05-12 · **Untersucht von:** Tobias Klein · **Bereich:** Scope 3, Kat. 1 (eingekaufte Güter) · **Status:** Ursache bestätigt, Korrektur in Umsetzungsplan eingeplant

## Symptom

Beim Probelauf der Umstellung einzelner Stahl-Positionen von spend-based auf supplier-specific fiel auf, dass die Summe der Kat.-1-Emissionen plausibel zu **hoch** wirkt — die spend-based-Schätzung lag ~12 % über der Summe aus mengenbasierten Lieferantendaten für dieselben Materialien.

## Untersuchung

1. Spend-Positionen je Materialgruppe gegen Lieferanten-Mengen abgeglichen.
2. Festgestellt: Einige Spend-Positionen umfassen **weiterverarbeitete Vormaterialien**, deren Rohmaterial-Spend separat bereits erfasst war.
3. Der generische spend-based-Faktor (`../../../../object-model/objects/ef-stahl-spend-based.md`) zählt damit Teile der Wertschöpfung doppelt.

## Ursache

Spend-based-Bilanzierung mit Brutto-Spend ohne Bereinigung um interne Wertschöpfungsstufen → Doppelzählung an Materialschnittstellen.

## Korrektur

- Bei Umstellung auf supplier-specific (Plan-Paket 6, `../../plans/scope-3/supplier-data-collection.md`) wird mengenbasiert gerechnet → Problem entfällt für umgestellte Lieferanten.
- Für noch spend-based verbleibende Tail-Lieferanten: Spend um identifizierte Doppelpositionen bereinigen.
- Basisjahr 2024 muss nach Umstellung neu berechnet werden (sonst falscher Reduktions-Vergleich).

## Reporting-Auswirkung

Betrifft **ESRS E1-6** (Scope 3) und die ausgewiesene Reduktion vs. Basisjahr. Vor der CSRD-Offenlegung (`../../../reporting/esrs-datapoint-mapping.md`) muss die Korrektur abgeschlossen und dokumentiert sein — Wirtschaftsprüfer prüfen Konsistenz Basisjahr ↔ Berichtsjahr.
