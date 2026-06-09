#!/usr/bin/env python3
"""Modelliert jedes WESENTLICHE Thema aus -> Policy + Ziel + KPI + Initiative.

Da keine Vaillant-Originaldokumente vorliegen, sind die Werte **educated guesses**
(ESRS-typische Metriken/Zielwerte) — in jedem Objekt klar als Annahme markiert.
Eine kuratierte Wissensbasis (KB) liefert je Sub-Thema sinnvolle Metriken; der Rest
fällt auf standard-spezifische Defaults zurück.

Aufruf:  python3 tools/model_themes.py   ·  benötigt PyYAML.
"""
from __future__ import annotations
import re, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt")

ROOT = Path(__file__).resolve().parent.parent
OBJ = ROOT / "objects"
FM = re.compile(r"^(---\n.*?\n---)\n?(.*)$", re.DOTALL)
STAND = "2026-06-09"
UML = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
NOTE = "\n\n> **Educated Guess** — kein Vaillant-Originaldokument; plausible, ESRS-typische Annahme zur Ausmodellierung."


def norm(s):
    return (s or "").translate(UML).lower()


# KB: (Schlüssel-Substrings) -> (Policy, Ziel-Metrik+Einheit, Baseline, Ziel, Zieljahr, KPI, Initiative)
# Erst spezifische, dann generische Einträge (erste Übereinstimmung gewinnt).
KB = [
    (["klimawandel-mitigation"], ("Klimaschutz- & Transitionsplan (Reduktion vor Kompensation)",
      "THG absolut Scope 1-3", "Mt CO2e", 140, 70, 2035, "THG-Fußabdruck Scope 1-3", "Wärmepumpen-Hochlauf & Gasausstieg")),
    (["klimawandel-adaptation"], ("Klimaanpassungs-Richtlinie",
      "Standorte mit Klimarisiko-Assessment", "%", 40, 100, 2028, "Abdeckung Klimarisiko-Assessment", "Resilienz-Programm Produktionsstandorte")),
    (["energie"], ("Energiemanagement-Policy (ISO 50001)",
      "Energieintensität", "Index (2024=100)", 100, 80, 2030, "Energieintensität", "Effizienzprogramm Werke")),
    (["luftverschmutzung"], ("Luftreinhaltungs-Policy",
      "NOx-/Feinstaub-Emissionen", "t/Jahr", 100, 60, 2030, "Luftschadstoff-Emissionen", "Filtertechnik-Nachrüstung")),
    (["besorgniserregende stoffe"], ("Chemikalien-/SVHC-Policy",
      "Anteil SVHC-freier Produkte", "%", 80, 100, 2030, "SVHC-Freiheit", "SVHC-Substitutionsprogramm")),
    (["wasser"], ("Wasser-Policy",
      "Wasserintensität", "Index (2024=100)", 100, 80, 2030, "Wasserintensität", "Wassereffizienz-Programm")),
    (["habitat", "oekosysteme", "arten", "biodivers"], ("Biodiversitäts- & No-Deforestation-Policy",
      "Lieferketten mit Biodiversitäts-Screening", "%", 10, 80, 2030, "Biodiversitäts-Screening-Abdeckung", "TNFD-LEAP vorgelagerte Metalle")),
    (["ressourcen-inflows"], ("Rohstoff- & Kreislauf-Policy",
      "Sekundärmaterial-/Rezyklat-Anteil", "%", 25, 40, 2030, "Rezyklat-Anteil", "CRM-Diversifizierung & Rezyklat-Einsatz")),
    (["outflows (abfall)", "outflows-abfall", "abfall"], ("Abfall- & Kreislauf-Policy",
      "Recyclingquote Abfall", "%", 80, 95, 2030, "Recyclingquote", "Zero-Waste-Programm")),
    (["outflows (produkte)", "produkte"], ("Ecodesign-Policy",
      "Recyclingfähigkeit der Produkte", "%", 70, 90, 2032, "Produkt-Recyclingfähigkeit", "Design-for-Recycling")),
    (["anti-korruption", "korruption"], ("Anti-Korruptions-Richtlinie / Code of Conduct",
      "Mitarbeitende mit Anti-Korruptions-Schulung", "%", 85, 100, 2027, "Schulungsabdeckung Anti-Korruption", "Compliance-Programm")),
    (["lieferantenbeziehungen"], ("Supplier Code of Conduct",
      "Lieferanten mit akzeptiertem Code of Conduct", "%", 70, 95, 2028, "CoC-Abdeckung Lieferanten", "Lieferanten-Management-Programm")),
    (["lobbying", "politischer einfluss"], ("Policy zu politischem Engagement & Lobbying",
      "Transparenz Lobbying (EU-Register)", "%", 80, 100, 2027, "Lobbying-Transparenz", "Public-Affairs-Governance")),
    (["zwangsarbeit"], ("Modern-Slavery- / Zwangsarbeit-Policy",
      "Hochrisiko-Lieferanten mit Zwangsarbeits-Audit", "%", 30, 100, 2028, "Audit-Abdeckung Zwangsarbeit", "Lieferketten-Sorgfalt (Polysilizium/3TG)")),
    (["kinderarbeit"], ("Kinderarbeit-Policy",
      "Hochrisiko-Lieferanten mit Kinderarbeits-Audit", "%", 30, 100, 2028, "Audit-Abdeckung Kinderarbeit", "3TG-/Kobalt-Due-Diligence")),
    (["menschenrechts", "programm-uplift"], ("Menschenrechts-Policy (UNGP/LkSG/CSDDD)",
      "Lieferanten mit Menschenrechts-Assessment", "%", 30, 90, 2028, "HRDD-Abdeckung", "Human-Rights-Due-Diligence-Programm")),
    (["gleiches entgelt", "gleichstellung"], ("Diversity- & Equal-Pay-Policy",
      "Gender Pay Gap", "%", 12, 5, 2030, "Gender Pay Gap", "Pay-Equity-Programm")),
    (["aus- und weiterbildung", "weiterbildung", "schulung"], ("Weiterbildungs-Policy",
      "Schulungsstunden je Mitarbeitende:r", "h/Jahr", 20, 35, 2030, "Schulungsstunden/MA", "Reskilling-Programm (Wärmepumpe)")),
    (["tarifverhandlung", "vereinigungsfreiheit", "sozialer dialog", "betriebsraete", "partizipation"],
      ("Social-Dialogue-Policy", "Tarifbindung (Collective Bargaining Coverage)", "%", 70, 90, 2030,
       "Tarifbindung", "Sozialpartnerschafts-Programm")),
    (["angemessene entlohnung"], ("Living-Wage-Policy",
      "Anteil mit existenzsicherndem Lohn", "%", 90, 100, 2028, "Living-Wage-Abdeckung", "Living-Wage-Programm")),
    (["sichere beschaeftigung"], ("Beschäftigungs-Policy",
      "Anteil unbefristeter Beschäftigung", "%", 88, 95, 2030, "Festanstellungs-Quote", "Stabile-Beschäftigung-Initiative")),
    (["work-life-balance"], ("Work-Life-Balance-Policy",
      "Überstundenquote", "%", 8, 4, 2030, "Überstundenquote", "Flexible-Arbeit-Programm")),
    (["sozialschutz"], ("Sozialschutz-Policy",
      "Sozialschutz-Abdeckung", "%", 95, 100, 2028, "Sozialschutz-Abdeckung", "Sozialschutz-Initiative")),
    (["nichtdiskriminierung", "anti-belaestigung", "gewalt"], ("Anti-Diskriminierungs- & Anti-Belästigungs-Policy",
      "Behandelte Diskriminierungs-/Belästigungsfälle", "% behoben", 80, 100, 2028, "Fallbehandlungs-Quote", "Respect-at-Work-Programm")),
    (["angemessene unterkunft", "arbeitszeit", "wasser und sanitaer", "sanitaer"], ("Arbeitsbedingungen-Policy",
      "Lieferanten-Audits zu Arbeitsbedingungen", "%", 30, 90, 2028, "Audit-Abdeckung Arbeitsbedingungen", "Lieferanten-Arbeitsbedingungen-Programm")),
    (["fpic", "selbstbestimmung", "kulturelle rechte", "landbezogene", "gemeinschaften", "menschenrechtsverteidiger"],
      ("Community- & Indigenous-Rights-Policy", "Projekte mit Community-/FPIC-Assessment", "%", 20, 100, 2030,
       "FPIC-/Community-Assessment-Abdeckung", "Community-Engagement-Programm")),
    (["verbraucher", "sicherheit der person", "schutz von kindern"], ("Produktsicherheits-Policy",
      "Sicherheitsrelevante Produktvorfälle", "Vorfälle/Jahr", 12, 3, 2030, "Produktsicherheits-Vorfälle", "Produktsicherheits-Programm (CO/Wartung)")),
    (["marketing"], ("Responsible-Marketing-Policy (Anti-Greenwashing)",
      "Beanstandete Werbeaussagen", "Fälle/Jahr", 5, 0, 2028, "Greenwashing-Beanstandungen", "Claims-Substantiation-Prozess")),
    (["zugang zu informationen"], ("Transparenz-Policy",
      "Produkte mit transparenter Effizienz-/Kosteninfo", "%", 70, 100, 2028, "Produkt-Transparenz", "Verbraucher-Transparenz-Initiative")),
    (["zugang zu produkten"], ("Erschwinglichkeits-Policy",
      "Förderfähige/erschwingliche Wärmepumpen-Modelle", "Modelle", 4, 10, 2030, "Erschwingliche WP-Modelle", "Affordability-Programm")),
    (["installateur"], ("Installateurs-Qualifizierungs-Policy",
      "Zertifizierte Installateure im Netzwerk", "Tsd.", 8, 20, 2030, "Zertifizierte Installateure", "Installer Academy")),
    (["waermepumpen-transformation"], ("Heat-Pump-Transformation-Strategie",
      "Umsatzanteil Wärmepumpen", "%", 30, 60, 2030, "WP-Umsatzanteil", "Wärmepumpen-Transformations-Programm")),
    (["gesundheit und sicherheit"], ("Arbeitssicherheits- & Gesundheits-Policy",
      "LTIFR", "Unfälle/1 Mio. h", 6, 3, 2030, "LTIFR", "Arbeitssicherheits-Programm")),
]
# (std, sub-substring) -> KB-Schlüssel-Override für gleichnamige Themen in versch. Standards
OVERRIDE = {
    ("S2", "gesundheit und sicherheit"): ("Lieferanten-Arbeitssicherheits-Policy",
      "Lieferanten mit H&S-Audit", "%", 30, 90, 2028, "H&S-Audit-Abdeckung Lieferkette", "Lieferketten-H&S-Programm"),
    ("S4", "gesundheit und sicherheit"): ("Produktsicherheits-Policy",
      "Sicherheitsrelevante Produktvorfälle", "Vorfälle/Jahr", 12, 3, 2030, "Produktsicherheits-Vorfälle", "Produktsicherheits-Programm (CO/Wartung)"),
}
STD_FALLBACK = {
    "E": ("Umwelt-Policy", "Umsetzungsgrad Umweltmaßnahmen", "%", 30, 100, 2030, "Umsetzungsgrad", "Umwelt-Maßnahmenprogramm"),
    "S": ("Sozial-/Menschenrechts-Policy", "Abdeckung Sorgfaltsmaßnahmen", "%", 30, 90, 2030, "Sorgfalts-Abdeckung", "Sozial-Sorgfaltsprogramm"),
    "G": ("Governance-Policy", "Umsetzungsgrad Governance-Kontrollen", "%", 70, 100, 2028, "Kontroll-Umsetzungsgrad", "Governance-Programm"),
    "E_S": ("Unternehmensspezifische Policy", "Umsetzungsgrad", "%", 30, 100, 2030, "Umsetzungsgrad", "Strategisches Programm"),
}


def lookup(std, sub):
    subn = norm(sub)
    if (std, _firstkey(subn)) in OVERRIDE:
        return OVERRIDE[(std, _firstkey(subn))]
    for keys, entry in KB:
        if any(k in subn for k in keys):
            return entry
    if std == "ES":
        return STD_FALLBACK["E_S"]
    return STD_FALLBACK.get(std[0], STD_FALLBACK["S"])


def _firstkey(subn):
    return "gesundheit und sicherheit" if "gesundheit und sicherheit" in subn else subn


def fm_of(text):
    m = FM.match(text)
    return yaml.safe_load(m.group(1).strip("-\n")), m.group(2)


def write(fid, fm, body):
    lines = ["---"] + [f"{k}: {v}" for k, v in fm.items()] + ["---", "", body, ""]
    (OBJ / f"{fid}.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    topics = []
    for p in OBJ.glob("topic-*.md"):
        fm, body = fm_of(p.read_text(encoding="utf-8"))
        if fm.get("status") == "wesentlich":
            topics.append((p, fm, body))
    n = 0
    for p, fm, body in topics:
        tid = fm["id"]; std = str(fm["esrs_bezug"]); base_id = tid[len("topic-"):]
        h = re.search(r"# Thema:\s*(.+)", body)
        sub = (h.group(1).strip() if h else base_id)
        pol, tname, unit, b, z, zj, kname, iname = lookup(std, sub)
        pid, gid, kid, iid = (f"policy-{base_id}", f"target-{base_id}",
                              f"kpi-{base_id}", f"initiative-{base_id}")
        write(kid, {"id": kid, "type": "kpi", "owner": "person-dma-lead", "status": "aktiv",
                    "stand": STAND, "review_zyklus": "P12M", "vertraulichkeit": "intern",
                    "esrs_bezug": std, "einheit": f'"{unit}"'},
              f"# KPI: {kname}\n\nMetrik für „{sub}“ ({std}). Einheit: {unit}." + NOTE)
        write(gid, {"id": gid, "type": "target", "owner": "person-dma-lead", "status": "geplant",
                    "stand": STAND, "review_zyklus": "P12M", "vertraulichkeit": "intern",
                    "esrs_bezug": std, "einheit": f'"{unit}"', "baseline_wert": b, "baseline_jahr": 2024,
                    "zielwert": z, "zieljahr": zj, "geltungsbereich": "Konzern",
                    "measured_by": f"[{kid}]", "supported_by": f"[{iid}]"},
              f"# Ziel: {tname} ({b} → {z} {unit} bis {zj})\n\nFür Thema „{sub}“ ({std})." + NOTE)
        write(iid, {"id": iid, "type": "initiative", "owner": "person-dma-lead", "status": "geplant",
                    "stand": STAND, "review_zyklus": "P12M", "vertraulichkeit": "intern",
                    "esrs_bezug": std, "supports": f"[{gid}]"},
              f"# Initiative: {iname}\n\nMaßnahme zur Erreichung des Ziels für „{sub}“ ({std})." + NOTE)
        write(pid, {"id": pid, "type": "policy", "owner": "person-dma-lead", "status": "in-kraft",
                    "stand": STAND, "review_zyklus": "P12M", "vertraulichkeit": "intern",
                    "esrs_bezug": std, "concerns": f"[{tid}]"},
              f"# Policy: {pol}\n\nESRS-Policy-Offenlegung für „{sub}“ ({std})." + NOTE)
        # Topic um Kanten erweitern (has_iro bleibt)
        fm.setdefault("has_target", []); fm.setdefault("has_kpi", []); fm.setdefault("has_initiative", [])
        fm["has_target"] = f"[{gid}]"; fm["has_kpi"] = f"[{kid}]"; fm["has_initiative"] = f"[{iid}]"
        write(tid, fm, body.strip())
        n += 1
    print(f"Ausmodelliert: {n} Themen × (Policy+Ziel+KPI+Initiative) = {n*4} neue Objekte")


if __name__ == "__main__":
    main()
