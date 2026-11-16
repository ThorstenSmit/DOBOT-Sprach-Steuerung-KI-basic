"""Sicherheitsgrenzen des Dobot Magician (mm bzw. Grad).

Entspricht den Werten aus 05_move_man.py des Grundprojekts. Diese Datei gibt es extra,
weil sich 05_move_man.py (beginnt mit einer Ziffer) nicht normal importieren lässt:

    from grenzen import GRENZEN, MAX_RADIUS, MAX_SCHRITT
"""

GRENZEN = {
    "x": (150.0, 300.0),
    "y": (-150.0, 150.0),
    "z": (0.0, 150.0),
    "r": (-90.0, 90.0),
}

MAX_RADIUS = 300.0   # größter erlaubter Abstand zur Basis, gerechnet aus x und y
MAX_SCHRITT = 150.0  # größte erlaubte Bewegung pro Befehl (mm)

HOME = (200.0, 0.0, 50.0, 0.0)  # sichere Ausgangsposition x, y, z, r
