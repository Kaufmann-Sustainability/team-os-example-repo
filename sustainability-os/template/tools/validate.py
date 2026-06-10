#!/usr/bin/env python3
"""Integritäts-Validator für den Objektgraphen (Grundproblem E, lauffähig).

Setzt durch, was eine schöne Architektur sonst nur erhofft:
  - jedes Objekt trägt die Pflicht-Metadaten
  - owner zeigt auf eine existierende person-id
  - jede getypte Beziehung zeigt auf ein existierendes Objekt erlaubten Typs
  - target-Regeln (Baseline/Zieljahr) stimmen
  - vertraulichkeit + review_zyklus sind formal gültig
Zusätzlich (Warnung, kein Fehler): überfällige Objekte (Frische-Check, Problem D).

Aufruf:  python3 tools/validate.py
Exit:    0 = sauber · 1 = Integritätsfehler
Benötigt: PyYAML.
"""
from __future__ import annotations
import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML benötigt:  pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = yaml.safe_load((ROOT / "object-schema.yaml").read_text(encoding="utf-8"))
FM = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

# Felder, die KEINE Objekt-Beziehungen sind, auch wenn sie in Frontmatter stehen.
NICHT_BEZIEHUNG = set(SCHEMA["metadata_pflicht"]) | set(SCHEMA["metadata_optional"]) | {
    "github", "slack", "rolle", "datum", "entscheidung", "einheit",
    "baseline_wert", "baseline_jahr", "zielwert", "zieljahr", "geltungsbereich",
    "betrag", "waehrung", "jahr",
}


def lade_objekte() -> dict[str, dict]:
    objekte: dict[str, dict] = {}
    for pfad in sorted((ROOT / "objects").glob("*.md")):
        m = FM.search(pfad.read_text(encoding="utf-8"))
        if not m:
            print(f"FEHLER  {pfad.name}: kein YAML-Frontmatter")
            continue
        data = yaml.safe_load(m.group(1)) or {}
        data["_datei"] = pfad.name
        objekte[data.get("id", pfad.stem)] = data
    return objekte


def pruefe(objekte: dict[str, dict]) -> list[str]:
    fehler: list[str] = []
    typen = SCHEMA["objekt_typen"]
    vokab = SCHEMA["beziehungs_vokabular"]

    def E(oid, msg):
        fehler.append(f"FEHLER  {oid}: {msg}")

    for oid, obj in objekte.items():
        # 1) Pflicht-Metadaten
        for feld in SCHEMA["metadata_pflicht"]:
            if feld not in obj:
                E(oid, f"Pflichtfeld '{feld}' fehlt")
        typ = obj.get("type")
        if typ not in typen:
            E(oid, f"unbekannter type '{typ}'")
            continue

        # 2) typ-spezifische Pflichtfelder
        for feld in typen[typ]["pflichtfelder"]:
            if feld not in obj:
                E(oid, f"type={typ} verlangt Feld '{feld}'")
        # 2b) "eines von" — mind. ein Feld je Gruppe muss vorhanden sein
        for gruppe in typen[typ].get("pflicht_eines", []):
            if not any(feld in obj for feld in gruppe):
                E(oid, f"type={typ} verlangt eines von {gruppe}")

        # 3) owner -> existierende person
        owner = obj.get("owner")
        if owner and (owner not in objekte or objekte[owner].get("type") != "person"):
            E(oid, f"owner '{owner}' ist keine existierende person-id")

        # 4) vertraulichkeit / review_zyklus formal
        if obj.get("vertraulichkeit") not in SCHEMA["vertraulichkeit_stufen"]:
            E(oid, f"vertraulichkeit '{obj.get('vertraulichkeit')}' ungültig")
        rz = obj.get("review_zyklus")
        if rz is not None and not re.fullmatch(r"P\d+M", str(rz)):
            E(oid, f"review_zyklus '{rz}' nicht im Format P<n>M")

        # 5) Beziehungen: erlaubt + Ziel existiert + Ziel-Typ erlaubt
        erlaubte = set(typen[typ]["beziehungen"])
        for feld, wert in obj.items():
            if feld in NICHT_BEZIEHUNG or feld.startswith("_") or feld == "type":
                continue
            if feld not in vokab:
                continue  # kein bekannter Kantentyp -> ignorieren (z.B. quelle-Pfade)
            if feld not in erlaubte:
                E(oid, f"Beziehung '{feld}' für type={typ} nicht erlaubt")
                continue
            ziele = wert if isinstance(wert, list) else [wert]
            zieltypen = vokab[feld]
            for ziel in ziele:
                if zieltypen == ["_extern_"]:          # darf auf Repo-Datei zeigen
                    # Pfad ist relativ zur Objekt-Datei notiert (liegt in objects/).
                    if not (ROOT / "objects" / ziel).resolve().exists():
                        E(oid, f"{feld}: externer Pfad '{ziel}' existiert nicht")
                    continue
                if ziel not in objekte:
                    E(oid, f"{feld}: Ziel '{ziel}' existiert nicht (tote Kante)")
                elif objekte[ziel].get("type") not in zieltypen:
                    E(oid, f"{feld}: Ziel '{ziel}' hat type "
                           f"'{objekte[ziel].get('type')}', erlaubt {zieltypen}")

        # 6) target-Regeln
        if typ == "target":
            bj, zj = obj.get("baseline_jahr"), obj.get("zieljahr")
            if isinstance(bj, int) and isinstance(zj, int) and not zj > bj:
                E(oid, f"zieljahr ({zj}) muss > baseline_jahr ({bj}) sein")
            for f in ("baseline_wert", "zielwert"):
                if not isinstance(obj.get(f), (int, float)):
                    E(oid, f"{f} muss numerisch sein")
    return fehler


def frische_warnungen(objekte: dict[str, dict]) -> list[str]:
    warn, heute = [], date.today()
    for oid, obj in objekte.items():
        rz, stand = obj.get("review_zyklus"), obj.get("stand")
        if not rz or not stand:
            continue
        m = re.fullmatch(r"P(\d+)M", str(rz))
        if not m:
            continue
        try:
            y, mo, d = map(int, str(stand).split("-"))
        except ValueError:
            continue
        faellig_monat = mo + int(m.group(1))
        faellig = date(y + (faellig_monat - 1) // 12, (faellig_monat - 1) % 12 + 1, d)
        if faellig < heute:
            warn.append(f"WARN    {oid}: überfällig (fällig {faellig}, owner {obj.get('owner')})")
    return warn


def main() -> int:
    objekte = lade_objekte()
    fehler = pruefe(objekte)
    warn = frische_warnungen(objekte)
    print(f"Geprüft: {len(objekte)} Objekte\n")
    for z in fehler + warn:
        print(z)
    if not fehler:
        print(f"\n✓ Integrität OK ({len(warn)} Frische-Warnung(en)).")
        return 0
    print(f"\n✗ {len(fehler)} Integritätsfehler.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
