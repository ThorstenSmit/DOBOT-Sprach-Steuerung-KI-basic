"""Anbindung an ein Cloud-LLM (OpenAI-kompatible Chat-API, z. B. Groq).

STUNDE 1: SYSTEM_PROMPT verbessern und frage_ki() ausprobieren.
STUNDE 3: Fehlerbehandlung ergänzen (siehe TODO).

Einstellungen kommen aus Umgebungsvariablen (siehe README.md), NIE aus dem Code:
    GROQ_API_KEY   dein API-Schlüssel
    GROQ_MODEL     Modellname (bekommst du von der Lehrkraft)
    KI_URL         optional, Standard: Groq
"""
import json
import os

import requests

KI_URL = os.environ.get("KI_URL", "https://api.groq.com/openai/v1/chat/completions")

# TODO (Stunde 1): Verbessere den Prompt. Was weiß die KI noch nicht? Was macht sie falsch?
SYSTEM_PROMPT = """\
Du übersetzt Befehle auf Deutsch in Steuerbefehle für einen Roboterarm (Dobot Magician).
Antworte AUSSCHLIESSLICH mit einem JSON-Objekt, ohne Text drumherum.

Koordinaten in Millimetern: x = nach vorn, y = nach links (+) / rechts (-), z = Höhe.

Erlaubte Formen:
{"aktion": "fahre_zu", "x": 200, "y": 0, "z": 50, "r": 0}
{"aktion": "fahre_relativ", "dx": 0, "dy": 50, "dz": 0}
{"aktion": "home"}
{"aktion": "saugnapf_an"}
{"aktion": "saugnapf_aus"}
"""


class KIFehler(Exception):
    """Alles, was beim Fragen der KI schiefgehen kann (Netz, Key, Format)."""


def frage_ki(text: str) -> dict:
    """Schickt den Nutzertext an die KI und gibt das Antwort-JSON als dict zurück."""
    schluessel = os.environ.get("GROQ_API_KEY")
    modell = os.environ.get("GROQ_MODEL")
    if not schluessel or not modell:
        raise KIFehler("GROQ_API_KEY oder GROQ_MODEL ist nicht gesetzt (siehe README.md).")

    # TODO (Stunde 3): Fange die Fehler gezielt ab und wirf jeweils einen KIFehler mit
    #   verständlicher Meldung:
    #     - requests.Timeout / requests.ConnectionError   (kein Internet)
    #     - HTTP 401 (Key falsch), 429 (Limit erreicht), andere Statuscodes
    #     - Antwort ist kein gültiges JSON (json.JSONDecodeError, KeyError)
    antwort = requests.post(
        KI_URL,
        headers={"Authorization": f"Bearer {schluessel}"},
        json={
            "model": modell,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0,
        },
        timeout=10,
    )
    antwort.raise_for_status()
    return json.loads(antwort.json()["choices"][0]["message"]["content"])
