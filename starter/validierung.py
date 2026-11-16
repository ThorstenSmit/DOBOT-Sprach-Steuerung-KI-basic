"""Der Sicherheits-Layer: Nichts, was die KI liefert, erreicht den Roboter ohne diese Prüfung.

STUNDE 3: Implementiere validiere(). Schreibe zuerst die Tests in test_validierung.py.
Bis dahin akzeptiert die Platzhalter-Version ALLES (unsicher!).
"""
from grenzen import GRENZEN, MAX_RADIUS, MAX_SCHRITT  # noqa: F401  (für deine Prüfungen)

WHITELIST = {"fahre_zu", "fahre_relativ", "home", "saugnapf_an", "saugnapf_aus"}


class UngueltigerBefehl(ValueError):
    """Der Befehl ist unzulässig und darf NICHT an den Roboter gehen."""


def validiere(befehl: dict, aktuelle_position=(200.0, 0.0, 50.0, 0.0)) -> dict:
    """Prüft einen Befehl. Gibt ihn zurück, wenn er zulässig ist, sonst UngueltigerBefehl.

    aktuelle_position: (x, y, z, r) des Roboters, nötig für 'fahre_relativ'
    (erst das Ziel berechnen, dann prüfen).
    """
    # TODO: Platzhalter, ersetzen! Prüfen:
    #   1. ist befehl ein dict und "aktion" in WHITELIST?
    #   2. fehlen Pflichtfelder? (fahre_zu: x,y,z,r  /  fahre_relativ: dx,dy,dz)
    #   3. sind alle Werte echte Zahlen (kein str, None, NaN, inf, bool)?
    #   4. Ziel innerhalb GRENZEN und Radius <= MAX_RADIUS?
    #   5. Schrittweite <= MAX_SCHRITT?
    return befehl
