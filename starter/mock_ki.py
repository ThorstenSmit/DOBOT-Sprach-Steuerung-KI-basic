"""Mock-KI mit festen Antworten, damit Oberfläche und Tests auch ohne Internet laufen.

Enthält absichtlich auch "schlechte" Antworten, wie sie eine echte KI liefern kann.
"""

BEISPIELE = {
    "home": {"aktion": "home"},
    "links": {"aktion": "fahre_relativ", "dx": 0, "dy": 50, "dz": 0},
    "rechts": {"aktion": "fahre_relativ", "dx": 0, "dy": -50, "dz": 0},
    "vor": {"aktion": "fahre_relativ", "dx": 50, "dy": 0, "dz": 0},
    "saugnapf an": {"aktion": "saugnapf_an"},
    "saugnapf aus": {"aktion": "saugnapf_aus"},
    # --- absichtlich fehlerhaft: die Validierung muss diese ablehnen ---
    "5 meter": {"aktion": "fahre_relativ", "dx": 0, "dy": 0, "dz": 5000},
    "tisch": {"aktion": "fahre_zu", "x": 200, "y": 0, "z": -40, "r": 0},
    "formatiere": {"aktion": "loesche_festplatte"},
    "text": {"aktion": "fahre_zu", "x": "weit weg", "y": 0, "z": 50, "r": 0},
}


def frage_mock(text: str) -> dict:
    """Wie frage_ki(), liefert aber feste Antworten nach Stichwort."""
    klein = text.lower()
    for stichwort, antwort in BEISPIELE.items():
        if stichwort in klein:
            return dict(antwort)
    return {"aktion": "unbekannt"}
