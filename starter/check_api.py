"""Prüft in wenigen Sekunden, ob die KI-Anbindung funktioniert (Key, Modell, Internet).

Aufruf:  python check_api.py
"""
import requests

from ki_client import KIFehler, frage_ki

print("Frage die KI: 'Fahre zur Home-Position' ...")
try:
    print("Antwort:", frage_ki("Fahre zur Home-Position"))
    print("OK - die KI-Anbindung funktioniert.")
except KIFehler as e:
    print("FEHLER:", e)
except requests.exceptions.HTTPError as e:
    code = e.response.status_code
    hinweise = {
        401: "Key falsch oder abgelaufen (GROQ_API_KEY prüfen).",
        404: "Modellname oder URL falsch (GROQ_MODEL / KI_URL prüfen).",
        429: "Limit erreicht. Kurz warten und erneut versuchen.",
    }
    print(f"HTTP-Fehler {code}:", hinweise.get(code, e.response.text[:200]))
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    print("FEHLER: Keine Verbindung (Internet? Firewall/Proxy der Schule?)")
except Exception as e:  # noqa: BLE001
    print("FEHLER:", type(e).__name__, e)
