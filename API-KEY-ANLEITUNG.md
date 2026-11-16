# Eigenen API-Key bei Groq anlegen

Für das Projekt braucht dein Team Zugriff auf eine Cloud-KI. Die Lehrkraft kann dir einen Schlüssel geben. **Oder du legst selbst einen kostenlosen Account bei Groq an.** Diese Anleitung zeigt, wie. Du brauchst sie nur, wenn die Lehrkraft das möchte oder erlaubt.

> Die Oberfläche der Website kann von dieser Beschreibung abweichen, Websites ändern sich häufig. Der Ablauf bleibt aber gleich.

## Vorher klären
- **Nutzungsbedingungen:** Lies kurz die Bedingungen von Groq. Frage die Lehrkraft, wenn du unsicher bist, ob du als Schüler/-in einen Account anlegen darfst (z. B. wegen Altersgrenzen).
- **Persönliche Daten:** Gib in Prompts **keine** Namen, Adressen oder andere persönliche Daten ein. Eure Eingaben gehen an einen Server im Internet.
- **Geheimnis:** Ein API-Key ist wie ein Passwort. Wer ihn hat, kann in deinem Namen die KI nutzen.

## Schritt 1: Account anlegen
1. <https://console.groq.com> öffnen.
2. Registrieren (E-Mail-Adresse oder Anmeldung über einen vorhandenen Dienst) und ggf. die E-Mail bestätigen.

## Schritt 2: API-Key erstellen
1. In der Konsole den Bereich **API Keys** öffnen.
2. **Create API Key** wählen.
3. Einen Namen eingeben, z. B. `dobot-projekt`.
4. **Den Key sofort kopieren.** Er wird nur **einmal** angezeigt. Verlierst du ihn, erstellst du einfach einen neuen.

## Schritt 3: Key sicher verwenden
Der Key kommt **nie** in den Code, nie in Git, nie in Chats und nie in Screenshots. Setze ihn nur als Umgebungsvariable (PowerShell). Den Modellnamen bekommst du von der Lehrkraft:

```powershell
$env:GROQ_API_KEY = "dein-key"
$env:GROQ_MODEL   = "modellname-von-der-lehrkraft"
```
Das gilt nur für das aktuelle Terminal. Für dauerhaft siehe [starter/README.md](starter/README.md), Abschnitt 2.

## Schritt 4: Testen
Mit dem Starter-Paket (siehe [starter/README.md](starter/README.md)):
```powershell
python check_api.py
```
Erwartet: `OK - die KI-Anbindung funktioniert.`

| Meldung | Bedeutung und Lösung |
|---|---|
| HTTP 401 | Key falsch kopiert oder abgelaufen. Key prüfen oder neuen erstellen. |
| HTTP 404 | Modellname falsch. Genau so schreiben, wie ihn die Lehrkraft vorgibt. |
| HTTP 429 | Zu viele Anfragen (Limit des kostenlosen Plans). Kurz warten. |
| Keine Verbindung | Internet oder Firewall der Schule blockiert den Zugriff. Lehrkraft fragen. |

## Wenn der Key doch einmal veröffentlicht wurde
Du hast ihn versehentlich in Git oder einen Chat gestellt? **Sofort** in der Konsole unter **API Keys** löschen und einen neuen erstellen. Danach den alten Key auch aus dem Projektverlauf entfernen lassen (Lehrkraft fragen).

## Nach dem Projekt
Lösche deinen Key in der Konsole unter **API Keys**, damit er nicht mehr missbraucht werden kann.
