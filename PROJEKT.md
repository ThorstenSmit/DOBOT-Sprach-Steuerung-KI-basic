# Projekt: „Sprich mit dem Roboter“ – KI-gesteuerter Dobot Magician

## Die Projektfrage

> **Wie kann ein Roboterarm per natürlicher Sprache gesteuert werden, ohne dass er einer fehlerhaften KI-Antwort blind vertraut?**

Eine KI kann Befehle wie *„Fahre in die linke Ecke“* in Koordinaten übersetzen. Sie kann sich aber auch irren oder Dinge erfinden („halluzinieren“). Ein Roboter, der solche Werte ungeprüft ausführt, rammt den Tisch oder gefährdet Menschen. **Deine Aufgabe als Entwickler/in:** das „Gehirn“ (KI) und den „Körper“ (Dobot) über eine **robuste, sichere Middleware** verbinden.

Dieses Projekt trainiert, was bleibt, wenn KI Standardcode schreibt: Schnittstellen entwerfen, Daten validieren, Fehler abfangen und Verantwortung für Sicherheit übernehmen.

## Voraussetzungen
- Das Grundprojekt [DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement) läuft in **deinem eigenen Clone**: Der Dobot verbindet sich und `python 02_erste_bewegung.py` fährt.
- Du hast das **Starter-Paket** (Ordner `starter/`, Anleitung in [starter/README.md](starter/README.md)) in den Hauptordner deines Clones kopiert und `pip install -r requirements-ki.txt` ausgeführt.
- Du hast von der Lehrkraft **API-Schlüssel und Modellnamen** bekommen und `python check_api.py` meldet „OK“.

## Zeitplan: 4 Stunden in 2 Wochen

| | LF 11a – Funktionalität | LF 10a – Benutzerschnittstelle |
|---|---|---|
| **Woche 1** | **Stunde 1:** Mechanik, Befehlsschema, KI-Anbindung | **Stunde 2:** Bedienoberfläche mit Vorschau und Bestätigung |
| **Woche 2** | **Stunde 3:** Validierung, Tests, Fehlerbehandlung | **Stunde 4:** Zusammenbau, Stopp, Abnahme |

Arbeitet in **Zweierteams**. Es gibt nur einen Dobot-Zugang gleichzeitig, deshalb entwickelt und testet ihr Stunde 1 bis 3 größtenteils **ohne Roboter** und fahrt nur zum Test am Dobot.

### Architektur
```
 Texteingabe ──► KI-Client ──► JSON-Parser ──► VALIDIERUNG ──► Bestätigung ──► Dobot
 "Fahre nach     (Cloud-API,   (Schema-         (Grenzen,       (Vorschau,     (pydobot,
  links"          Timeout)      Prüfung)         Whitelist)      j/N)           STOPP)
                       │              │               │
                       └──────── Fehler? ─► Roboter bleibt stehen, Meldung an Nutzer
```
Grundregel: **Nichts, was die KI liefert, erreicht den Roboter ohne Validierung.**

---

## Stunde 1 (LF 11a): Mechanik, Befehlsschema, KI-Anbindung

### 1.1 Mechanik kurz erkunden (ca. 15 min)
Koordinatensystem: x vorn, y links/rechts, z Höhe, r Drehung, alles in mm (siehe [README](https://github.com/ThorstenSmit/DobotBasicMovement)). Fahrt mit der Weboberfläche des Grundprojekts an die Ränder des Arbeitsbereichs und **notiert**: Welche Werte sind erreichbar? Wo bleibt der Arm stehen und warum? (Schutzgrenzen: `GRENZEN` und `MAX_RADIUS` in `05_move_man.py`, für euren Code in `grenzen.py`.)

Schreibt `01_home.py` (Grenzwerte und `HOME` stehen in `grenzen.py`): verbinden (`verbinde()`), Ist-Position mit `device.pose()` ausgeben, sichere Home-Position anfahren, z. B. `move_to(200, 0, 50, 0, wait=True)`, am Ende `device.close()` (auch bei Fehlern, mit `try/finally`).

### 1.2 Das Befehlsprotokoll festlegen
Eine KI liefert Fließtext („Klar, ich bewege den Arm!“). Der Roboter braucht typisierte Parameter. Legt ein **festes Schema** fest. Vorschlag:

```json
{ "aktion": "fahre_zu", "x": 200, "y": 50, "z": 50, "r": 0 }
```
Erlaubte `aktion`-Werte (**Whitelist**): `fahre_zu` (absolut), `fahre_relativ` (Deltas `dx`, `dy`, `dz`), `home`, `saugnapf_an`, `saugnapf_aus`. Alles andere wird abgelehnt.

> **Diskussion im Team:** Absolute oder relative Koordinaten? Welche Fehlerquellen bringt „50 mm nach links“ mit sich (Bezug: aktuelle Position, Richtung von y)? Dokumentiert eure Entscheidung.

### 1.3 KI anbinden
- Schickt per `requests.post` eine Anfrage an die Chat-API (OpenAI-kompatibel). Der **JSON-Modus** (`response_format: {"type": "json_object"}`) und ein strenger **System-Prompt** sorgen dafür, dass nur JSON zurückkommt. Der System-Prompt beschreibt Schema, Whitelist, Einheiten und Koordinatensystem. Verbessert ihn iterativ und protokolliert Änderungen.
- **API-Key niemals im Code oder in Git!** Lest ihn aus einer Umgebungsvariable (`os.environ["GROQ_API_KEY"]`).
- Setzt immer einen **Timeout** (z. B. 10 s) und fangt `requests.RequestException` ab.

Das Gerüst liegt im Starter-Paket in `ki_client.py` (so sieht es aus):
```python
import os, json, requests

def frage_ki(text: str) -> dict:
    antwort = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
        json={
            "model": os.environ.get("GROQ_MODEL", "<Modellname von der Lehrkraft>"),
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
```

**Ergebnis Stunde 1:** `01_home.py` läuft, das Schema ist dokumentiert, `frage_ki("Fahre nach links")` liefert ein JSON-Objekt.

---

## Stunde 2 (LF 10a): Bedienoberfläche

**Ziel:** Eine Oberfläche gestalten, über die ein Mensch den KI-Vorschlag **versteht, prüft und bestätigt**, bevor sich der Roboter bewegt.

Verbessert die Konsolenanwendung `ki_steuerung.py` aus dem Starter-Paket (oder baut wahlweise eine Tkinter-/Weboberfläche; `app.py` des Grundprojekts dient als Vorlage):
```
> Fahre in die linke Ecke
KI-Vorschlag:  fahre_zu  x=200  y=100  z=50  r=0
Prüfung:       OK
Ausführen? [j/N]
```

**Anforderungen**
- **Vorschau (Dry-Run):** Zuerst anzeigen, was passieren würde, ausgeführt wird erst nach Bestätigung.
- **Verständliche Fehlermeldungen:** Nutzer bekommen klare Sätze („Keine Verbindung zur KI“), keine Stacktraces.
- **Rückmeldung:** Während die KI antwortet und der Roboter fährt, sieht der Nutzer einen Status („Frage KI ...“, „Fahre ...“).
- **Abbrechen jederzeit** möglich (leere Eingabe oder `exit`).
- Bis die Validierung (Stunde 3) fertig ist, nutzt ihr die **Platzhalter-Funktion** `validiere()` (akzeptiert alles) und die **Mock-KI** `mock_ki.py` (feste Beispielantworten), damit ihr die Oberfläche auch ohne Internet testet: `python ki_steuerung.py --mock --ohne-roboter`.

**Ergebnis Stunde 2:** Die Oberfläche läuft mit Mock-KI und Platzhalter-Validierung, der Dobot kann mit festen Beispielbefehlen angesteuert werden.

---

## Stunde 3 (LF 11a): Validierung, Tests, Fehlerbehandlung

### 3.1 Der Sicherheits-Layer (wichtigster Teil!)
Implementiert `validiere()` in `validierung.py` (Platzhalter ist vorgegeben). Sie **ungültige Befehle ablehnt (Exception)** und gültige zurückgibt. Prüft mindestens:
- Ist `aktion` in der Whitelist? Sind alle Pflichtfelder vorhanden?
- Sind die Werte **Zahlen** (kein Text, kein `null`, kein `NaN`)?
- Liegen die Zielwerte innerhalb von `GRENZEN` **und** `MAX_RADIUS`? Bei relativen Befehlen: erst das Ziel berechnen, dann prüfen!
- Ist die Schrittweite plausibel (z. B. nie mehr als 150 mm pro Befehl)?

**Schreibt zuerst die Tests** in `test_validierung.py` (zwei sind vorgegeben, Start mit `python -m pytest -v`):

| Eingabe | Erwartung |
|---|---|
| `fahre_zu` x=200, y=0, z=50 | akzeptiert |
| `fahre_zu` z=5000 | abgelehnt |
| `fahre_zu` z=-20 | abgelehnt (Tischkollision) |
| `fahre_zu` x=0, y=0 | abgelehnt (zu nah an der Basis / außer Reichweite) |
| `fahre_zu` x=300, y=150 | abgelehnt (Radius > `MAX_RADIUS`) |
| `aktion: "loesche_festplatte"` | abgelehnt (nicht in Whitelist) |
| `x: "viel"` | abgelehnt (kein Zahlenwert) |
| `fahre_relativ` führt aus dem Bereich heraus | abgelehnt |

Die Validierung lässt sich **ohne Hardware** testen.

### 3.2 Fehlerbehandlung
Fangt gezielt ab: Netzwerkfehler (Timeout, kein Internet), HTTP-Fehler (401 falscher Key, 429 Limit erreicht), Formatfehler (kein gültiges JSON) und Plausibilitätsfehler (Validierung lehnt ab). Wo im Code wird jeweils abgefangen? In allen Fällen gilt: **Der Roboter bekommt keinen Befehl.**

**Ergebnis Stunde 3:** Alle Tests grün, Fehlerfälle werden abgefangen und gemeldet.

---

## Stunde 4 (LF 10a): Zusammenbau, Stopp, Abnahme

1. **Integration:** Tauscht Mock-KI gegen `frage_ki()` und Platzhalter gegen die echte `validiere()`. Anschluss an den Dobot über `device.move_to(..., wait=True)` bzw. `device.suck(...)`; `device.close()` am Ende, auch bei Fehlern.
2. **Stopp:** Strg+C bzw. `device.stopp()` aus `dobot_helper.py` bricht sofort ab. Dobot-Schalter bleibt der echte Not-Aus.
3. **Abnahme-Challenge:** Löst folgende Fälle **gezielt aus** und zeigt, dass der Roboter stehen bleibt und eine verständliche Meldung erscheint:

| Fall | Wie auslösen? | Erwartetes Verhalten |
|---|---|---|
| Internet weg | WLAN trennen / falsche URL | Timeout, Meldung, kein Absturz |
| API-Key falsch / Limit erreicht | falschen Key setzen | Meldung (HTTP 401/429), kein Roboterbefehl |
| KI liefert kein JSON | Prompt absichtlich kaputt machen | Parser-Fehler abgefangen, kein Befehl |
| KI halluziniert Koordinaten | Eingabe: „Fahre 5 Meter nach oben“ | Validierung lehnt ab |
| Dobot antwortet nicht | Kabel ziehen / Dobot aus | Fehlermeldung, sauberes Beenden |

4. **Kurzpräsentation** (je Team ca. 3 min): Live-Demo eines gültigen Befehls und eines abgelehnten Befehls, dazu eine Antwort auf eine Reflexionsfrage.

**Ergebnis Stunde 4:** Lauffähiges System, abgenommene Challenge, kurze Präsentation.

---

## Erweiterungen (für Schnelle)
- **Offline-Fallback:** regelbasierter Parser („links“, „rechts“, „hoch“), falls die KI nicht erreichbar ist.
- **Mehrschrittige Befehle:** „Fahre ein Quadrat“ liefert eine **Liste** von Befehlen, die jeweils einzeln validiert werden.
- **Pick & Place** mit Saugnapf: „Nimm das Teil auf und lege es 10 cm weiter links ab.“
- **Protokolldatei:** Zeit, Eingabe, KI-Antwort, Prüfergebnis, Ausführung.

## Bewertungskriterien
| Kriterium | Beschreibung |
|---|---|
| Funktion | Befehl wird korrekt in eine Bewegung umgesetzt |
| Sicherheit | Validierung lehnt alle Testfälle korrekt ab, Tests vorhanden |
| Robustheit | Alle Fehlerfälle der Abnahme-Challenge sind abgefangen |
| Bedienbarkeit | Vorschau, verständliche Meldungen, Abbruch möglich (LF 10a) |
| Code-Qualität | Trennung in Funktionen/Module (KI-Client, Validierung, Oberfläche, Roboter), lesbar, kommentiert |
| Geheimnisse | Kein API-Key im Code oder Repository |
| Dokumentation | Schema, System-Prompt und Entscheidungen (absolut/relativ …) dokumentiert |

## Reflexionsfragen
1. Warum darf man der Ausgabe einer KI nie blind vertrauen, selbst bei „Temperatur 0“?
2. Welche Prüfungen gehören in die Middleware und welche in den Roboter-Treiber?
3. Was ändert sich, wenn nicht ein Dobot, sondern ein Gabelstapler gesteuert wird?
4. Welche Daten verlassen beim API-Aufruf den Rechner? (Datenschutz)

## Sicherheit am Roboter
- Arbeitsbereich frei halten, nie in den Arm greifen, solange er fährt.
- Nur eine Person bedient den Roboter, die anderen halten Abstand.
- Bei Fehlverhalten sofort den **Dobot am Schalter ausschalten**.
