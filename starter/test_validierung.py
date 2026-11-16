"""Tests für validiere(). Ausführen:  python -m pytest -v

Zwei Tests sind vorgegeben. Ergänze die übrigen Fälle aus der Tabelle in PROJEKT.md.
Mit der Platzhalter-Version sind die Ablehnungs-Tests ROT. Das ist gewollt (red -> green).
"""
import pytest

from validierung import UngueltigerBefehl, validiere


def test_gueltiger_befehl_wird_akzeptiert():
    befehl = {"aktion": "fahre_zu", "x": 200, "y": 0, "z": 50, "r": 0}
    assert validiere(befehl) == befehl


def test_zu_hohes_z_wird_abgelehnt():
    with pytest.raises(UngueltigerBefehl):
        validiere({"aktion": "fahre_zu", "x": 200, "y": 0, "z": 5000, "r": 0})


# TODO: weitere Tests
#   - z = -20                             -> abgelehnt (Tischkollision)
#   - x = 0, y = 0                        -> abgelehnt (zu nah an der Basis)
#   - x = 300, y = 150                    -> abgelehnt (Radius > MAX_RADIUS)
#   - aktion "loesche_festplatte"         -> abgelehnt (nicht in der Whitelist)
#   - x = "viel"                          -> abgelehnt (kein Zahlenwert)
#   - fahre_relativ aus dem Bereich       -> abgelehnt (Ziel berechnen!)
#   - float("nan"), None, True            -> abgelehnt
