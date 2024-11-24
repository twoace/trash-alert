# Trash Alert with Philips Hue Integration

Dieses Projekt ermöglicht es, eine Philips Hue-Lampe basierend auf Kalenderereignissen zu steuern. Die Lampe zeigt eine Farbe, die mit bestimmten Ereignistiteln in Ihrem Kalender verknüpft ist. Wenn mehrere Ereignisse gleichzeitig aktiv sind, wechselt die Lampe sanft zwischen den zugehörigen Farben.

## Funktionen

- **Kalenderintegration (CalDAV):**
  - Liest Kalenderereignisse aus einem Apple-Kalender oder anderen CalDAV-kompatiblen Kalenderdiensten.
- **Philips Hue-Steuerung:**
  - Verwendet die Philips Hue API, um die Lampe basierend auf Kalenderereignissen zu steuern.
- **Farbanzeige:**
  - Setzt Farben auf Basis eines Ereignistitels, mit Unterstützung für benutzerdefinierte Farbmappings.
- **Farbwechsel:**
  - Bei mehreren aktiven Ereignissen wird die Lampe alle 5 Sekunden auf die nächste Farbe umgestellt, mit einer schnellen Transition (0,5 Sekunden).

## Voraussetzungen

### Hardware
- Philips Hue Bridge eine Philips Hue-Lampe (Color).

### Bibliotheken
- `phue` – Für die Steuerung der Philips Hue-Lampen.
- `caldav` – Für den Zugriff auf CalDAV-kompatible Kalender.
- `python-dotenv` – Zum Laden von Umgebungsvariablen aus einer `.env`-Datei.
- `pytz` – Zum Einstellen der lokalen Zeit

## .env Datei Konfiguration

Die `.env`-Datei enthält alle wichtigen Konfigurationsparameter für das Projekt. Diese Datei sollte sich im `app`-Verzeichnis befinden und sensible Daten wie Benutzernamen, Passwörter und API-Keys enthalten. 

### Beispiel `.env`-Datei

```dotenv
# Philips Hue Konfiguration
HUE_BRIDGE_IP=192.168.x.x          # IP-Adresse Ihrer Hue-Bridge

# CalDAV Kalender Konfiguration
CALDAV_URL=https://caldav.icloud.com         # URL Ihres CalDAV-Servers
CALDAV_USERNAME=your_username               # Benutzername für den Kalender
CALDAV_PASSWORD=your_password               # Passwort für den Kalender
CALENDAR_NAME=YourCalendarName            # Name des Kalenders

# Lampe und Logging
LIGHT_NAME=YourLightName                  # Name der Lampe, die gesteuert wird
LOG_LEVEL=INFO                              # Log-Level (DEBUG, INFO, WARNING, ERROR)
