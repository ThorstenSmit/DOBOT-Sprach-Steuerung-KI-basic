# Starter-Paket „Sprich mit dem Roboter“

Dieses Paket enthält das Gerüst für das Projekt (siehe [../PROJEKT.md](../PROJEKT.md)). Du arbeitest in **deinem eigenen Clone** von [DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement).

## 1. Einrichten (einmalig, ca. 10 Minuten)

1. Grundprojekt klonen und einrichten, falls noch nicht geschehen (siehe `INSTALLREADME.md` des Grundprojekts). **Der Dobot muss mit `python 02_erste_bewegung.py` fahren.**
2. **Alle Dateien aus diesem `starter`-Ordner** (außer dieser README) in den Hauptordner deines Clones kopieren, also in denselben Ordner wie `dobot_helper.py`:
   ```
   DobotBasicMovement/
     dobot_helper.py        <- schon da
     grenzen.py             <- aus dem Starter
     ki_client.py
     mock_ki.py
     validierung.py
     test_validierung.py
     check_api.py
     ki_steuerung.py
     requirements-ki.txt
   ```
   Wichtig: Die Dateien müssen im selben Ordner liegen, sonst funktioniert `from dobot_helper import verbinde` nicht.
3. Im Terminal mit aktivierter Umgebung (`.venv\Scripts\Activate.ps1`) die Pakete installieren:
   ```powershell
   pip install -r requirements-ki.txt
   ```

## 2. API-Schlüssel setzen (PowerShell)

Schlüssel und Modellname bekommst du von der Lehrkraft. Oder du legst einen eigenen Key an: [../API-KEY-ANLEITUNG.md](../API-KEY-ANLEITUNG.md). **Der Schlüssel gehört nie in den Code, nie in Git und nie in einen Chat.**

Nur für das aktuelle Terminal:
```powershell
$env:GROQ_API_KEY = "dein-schluessel"
$env:GROQ_MODEL   = "modellname-von-der-lehrkraft"
```
Dauerhaft (gilt erst in einem **neuen** Terminal, ggf. VS Code neu starten):
```powershell
setx GROQ_API_KEY "dein-schluessel"
setx GROQ_MODEL   "modellname-von-der-lehrkraft"
```

## 3. Prüfen
```powershell
python check_api.py
```
Erwartet: `OK - die KI-Anbindung funktioniert.` Bei Fehlern zeigt das Skript Hinweise (Key falsch, Modell falsch, Limit, kein Internet).

Ohne Internet und ohne Dobot kannst du trotzdem arbeiten:
```powershell
python ki_steuerung.py --mock --ohne-roboter
```
Probiere Eingaben wie `home`, `links`, `5 meter nach oben` oder `tisch`. Die letzten beiden sind **absichtlich fehlerhaft**, die Validierung muss sie später ablehnen.

## 4. Die Dateien

| Datei | Was drin ist | Wann bearbeiten |
|---|---|---|
| `grenzen.py` | Sicherheitsgrenzen des Dobot | nur lesen |
| `ki_client.py` | `frage_ki()` und `SYSTEM_PROMPT` | Stunde 1 und 3 |
| `mock_ki.py` | Mock-KI mit festen Antworten (auch fehlerhaften) | bei Bedarf erweitern |
| `ki_steuerung.py` | Konsolenanwendung (Eingabe, Vorschau, Ausführung) | Stunde 2 und 4 |
| `validierung.py` | `validiere()`, zunächst **Platzhalter, der alles akzeptiert** | Stunde 3 |
| `test_validierung.py` | Tests, zwei vorgegeben | Stunde 3 (zuerst!) |
| `check_api.py` | Schnelltest der KI-Verbindung | nur ausführen |

Tests starten:
```powershell
python -m pytest -v
```

## 5. Regeln
- Nur eine Person pro Team bedient den Dobot, Arbeitsbereich frei, Dobot-Schalter in Reichweite.
- Vor dem Start der Skripte mit Dobot: die Weboberfläche des Grundprojekts (`app.py`), DobotLink und DobotLab beenden. Der Dobot hat nur einen Zugriff.
- Kein `git add` mit Schlüsseln. Prüfe vor jedem Commit mit `git status`, was hineinkommt.
