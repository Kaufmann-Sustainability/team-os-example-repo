# Glossar — kanonische Definitionen

> **Single Source of Truth für alle Begriffe und Kennzahlen.** Einträge werden über den `sustainability-standard`-Skill erstellt/aktualisiert, damit sie konsistent und vollständig sind. Andere Dokumente (inkl. Root-`CLAUDE.md`) verweisen hierher, statt eigene Definitionen zu führen.

### CSRD
- **Definition:** Corporate Sustainability Reporting Directive — EU-Richtlinie zur verpflichtenden Nachhaltigkeitsberichterstattung im Lagebericht.
- **Abgrenzung:** Die *Richtlinie*; die konkreten Standards darunter sind die ESRS.
- **Einheit / Berechnung:** —
- **ESRS-Bezug:** rahmenübergreifend
- **Synonyme:** —
- **Owner:** Markus Bauer · **Stand:** 2026-06-09

### Emissionsfaktor (EF)
- **Definition:** Umrechnungswert, der Aktivitätsdaten (z. B. kWh, t Material) in tCO₂e überführt.
- **Abgrenzung:** Nicht die Emission selbst — erst Aktivitätsdaten × EF ergibt die Emission.
- **Einheit / Berechnung:** z. B. kgCO₂e/kWh, kgCO₂e/t; gepflegt in `carbon-data/emission-factors-catalog.yaml`
- **ESRS-Bezug:** E1-6
- **Synonyme:** EF
- **Owner:** Sophie Wagner · **Stand:** 2026-06-09

### Doppelte Wesentlichkeit
- **Definition:** Bewertung von Nachhaltigkeitsthemen nach Impact-Wesentlichkeit (Auswirkung auf Mensch/Umwelt) *und* finanzieller Wesentlichkeit (Auswirkung auf das Unternehmen).
- **Abgrenzung:** Mehr als reine Risikobetrachtung — beide Richtungen sind erforderlich (ESRS-Pflicht).
- **Einheit / Berechnung:** —
- **ESRS-Bezug:** ESRS 2 / IRO
- **Synonyme:** double materiality
- **Owner:** Markus Bauer · **Stand:** 2026-06-09

### Scope 1
- **Definition:** Direkte THG-Emissionen aus eigenen oder kontrollierten Quellen (Verbrennung, Fuhrpark, Prozesse).
- **Abgrenzung:** Nicht eingekaufte Energie (= Scope 2).
- **Einheit / Berechnung:** tCO₂e = Aktivitätsdaten × EF
- **ESRS-Bezug:** E1-6
- **Synonyme:** direkte Emissionen
- **Owner:** Tobias Klein · **Stand:** 2026-06-09

### Scope 2
- **Definition:** Indirekte THG-Emissionen aus eingekaufter Energie (Strom, Wärme), ausgewiesen location- und market-based.
- **Abgrenzung:** Nur eingekaufte Energie; übrige indirekte Emissionen sind Scope 3.
- **Einheit / Berechnung:** tCO₂e = Verbrauch (kWh) × EF (location- bzw. market-based)
- **ESRS-Bezug:** E1-5, E1-6
- **Synonyme:** —
- **Owner:** Sophie Wagner · **Stand:** 2026-06-09

### Scope 3
- **Definition:** Alle übrigen indirekten Emissionen der Wertschöpfungskette (15 Kategorien lt. GHG Protocol), z. B. eingekaufte Güter, Transport, Produktnutzung.
- **Abgrenzung:** Weder eigene Quellen (Scope 1) noch eingekaufte Energie (Scope 2).
- **Einheit / Berechnung:** tCO₂e; Methodik je Kategorie (spend-based, supplier-specific, …)
- **ESRS-Bezug:** E1-6
- **Synonyme:** Wertschöpfungsketten-Emissionen
- **Owner:** Jonas Fischer · **Stand:** 2026-06-09

<!-- Neue Einträge über den `sustainability-standard`-Skill ergänzen, alphabetisch einsortiert. -->
<!-- Bekannte Lücke (im Review aufgefallen): „Prozessemissionen" ist noch nicht definiert. -->
