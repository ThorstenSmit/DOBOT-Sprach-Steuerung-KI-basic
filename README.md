# DOBOT-Sprach-Steuerung-KI-basic

**Projekt für Fachinformatiker/-innen Anwendungsentwicklung (3. Lehrjahr):** Ein Dobot Magician wird per natürlicher Sprache gesteuert. Eine Cloud-KI übersetzt Befehle wie *„Fahre in die linke Ecke“* in Roboterbefehle.

> **Projektfrage:** Wie kann ein Roboterarm per natürlicher Sprache gesteuert werden, ohne dass er einer fehlerhaften KI-Antwort blind vertraut?

Der Schwerpunkt liegt auf dem, was Entwickler/innen verantworten: **Schnittstellen entwerfen, KI-Antworten validieren, Fehler abfangen und Sicherheit gewährleisten.**

```
Texteingabe ──► KI-Client ──► JSON-Parser ──► VALIDIERUNG ──► Bestätigung ──► Dobot
```

## Einordnung: Vorstufe zu Physical AI
Dieses Projekt ist **keine vollständige Physical AI**, sondern eine **Vorstufe**: der erste Schritt in diese Richtung.

*Physical AI* meint Systeme, die die physische Welt **wahrnehmen**, selbst **entscheiden** und **handeln**, im Idealfall in einem **geschlossenen Regelkreis** (der Roboter prüft sein Ergebnis und korrigiert) und oft mit einer KI, die das Handeln selbst lernt oder steuert. Der Begriff ist unscharf.

| | Dieses Projekt |
|---|---|
| Wahrnehmung | nur Text (keine Sensoren) |
| Rolle der KI | **übersetzt** Sprache in einen Befehl (Parser) |
| Handeln | klassisch skriptiert, geprüft durch `validiere()` |
| Rückkopplung | keine (offene Kette) |
| Lernen | nein |

**Was ihr hier trotzdem lernt:** die Schicht *um* die KI herum, die jedes Physical-AI-System braucht: Schnittstellen entwerfen, KI-Antworten validieren, Fehler abfangen, Sicherheit.
**Wie es weitergeht:** [DOBOT-Vision-Steuerung-KI-advanced](https://github.com/ThorstenSmit/DOBOT-Vision-Steuerung-KI-advanced) ergänzt Kamera und eigenständige Entscheidungen. Danach folgt [DOBOT-Lernender-Greifer-KI-expert](https://github.com/ThorstenSmit/DOBOT-Lernender-Greifer-KI-expert): Der Roboter lernt aus eigener Erfahrung. Ohne Dobot: [PhysicalAI-Sortierweiche-Webcam-basic](https://github.com/ThorstenSmit/PhysicalAI-Sortierweiche-Webcam-basic) (Webcam, KI, Simulation oder SPS).

## Voraussetzung
Das Grundprojekt **[DobotBasicMovement](https://github.com/ThorstenSmit/DobotBasicMovement)** muss in deinem eigenen Clone laufen (Treiber, Python-Umgebung, `python 02_erste_bewegung.py` fährt).

## Los geht's
1. **[PROJEKT.md](PROJEKT.md)** lesen: Aufgabe, Zeitplan (4 Stunden in 2 Wochen), Teilaufgaben, Abnahme, Bewertungskriterien.
2. **[starter/README.md](starter/README.md)** folgen: Starter-Dateien in den Clone kopieren, Pakete installieren, API-Schlüssel setzen, `python check_api.py`.
3. **API-Schlüssel und Modellnamen** besorgen: entweder von der Lehrkraft oder mit einem eigenen kostenlosen Groq-Account nach **[API-KEY-ANLEITUNG.md](API-KEY-ANLEITUNG.md)**.

## Inhalt

| Pfad | Zweck |
|---|---|
| [PROJEKT.md](PROJEKT.md) | Projektbeschreibung und Aufgaben für Teams |
| [API-KEY-ANLEITUNG.md](API-KEY-ANLEITUNG.md) | Eigenen Groq-API-Key anlegen und sicher verwenden |
| [starter/](starter/) | Gerüst: KI-Client, Mock-KI, Validierungs-Platzhalter, Tests, Konsolenanwendung |

## Sicherheit
- API-Schlüssel gehören **nie** in Code, Git oder Chats.
- Am Roboter: Arbeitsbereich frei, nur eine Person bedient ihn, im Notfall den **Dobot-Schalter** ausschalten.

## Lizenz
MIT, siehe [LICENSE](LICENSE).
