"""Konsolenanwendung: Text -> KI -> Validierung -> Vorschau -> Bestätigung -> Dobot.

Start:
    python ki_steuerung.py --mock --ohne-roboter    # ohne Internet und ohne Dobot
    python ki_steuerung.py --mock                   # Mock-KI, aber echter Dobot
    python ki_steuerung.py                          # echte KI und echter Dobot

STUNDE 2 (LF 10a): Bedienoberfläche verbessern (Vorschau, Status, Meldungen, Abbruch).
STUNDE 3/4: echte validiere() und Fehlerbehandlung einbauen.
"""
import sys

from grenzen import HOME
from ki_client import KIFehler, frage_ki
from mock_ki import frage_mock
from validierung import UngueltigerBefehl, validiere

MOCK = "--mock" in sys.argv
OHNE_ROBOTER = "--ohne-roboter" in sys.argv


def zeige_vorschau(befehl: dict) -> None:
    # TODO (Stunde 2): übersichtliche, verständliche Darstellung
    print("KI-Vorschlag:", befehl)


def fuehre_aus(device, befehl: dict) -> None:
    """Setzt einen (validierten!) Befehl am Dobot um. device=None: nur simulieren."""
    aktion = befehl["aktion"]
    if device is None:
        print("(simuliert, kein Roboter angeschlossen)")
        return
    if aktion == "home":
        device.move_to(*HOME, wait=True)
    elif aktion == "fahre_zu":
        device.move_to(befehl["x"], befehl["y"], befehl["z"], befehl["r"], wait=True)
    elif aktion == "fahre_relativ":
        x, y, z, r, *_ = device.pose()
        device.move_to(x + befehl["dx"], y + befehl["dy"], z + befehl["dz"], r, wait=True)
    elif aktion == "saugnapf_an":
        device.suck(True)
    elif aktion == "saugnapf_aus":
        device.suck(False)


def main() -> None:
    device = None
    if not OHNE_ROBOTER:
        from dobot_helper import verbinde
        device = verbinde()
    try:
        print("Befehl eingeben (leer oder 'exit' beendet).")
        while True:
            text = input("> ").strip()
            if text in ("", "exit"):
                break
            try:
                # TODO (Stunde 3/4): Fehlerarten getrennt behandeln
                befehl = frage_mock(text) if MOCK else frage_ki(text)
                zeige_vorschau(befehl)
                pos = device.pose()[:4] if device else HOME
                befehl = validiere(befehl, pos)
                print("Prüfung:       OK")
            except UngueltigerBefehl as e:
                print("ABGELEHNT:", e)
                continue
            except KIFehler as e:
                print("KI-Fehler:", e)
                continue
            if input("Ausführen? [j/N] ").strip().lower() == "j":
                fuehre_aus(device, befehl)
    finally:
        if device is not None:
            device.close()


if __name__ == "__main__":
    main()
