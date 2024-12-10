# Trash Alert with Philips Hue Integration

Dieses Projekt ermöglicht es, eine Philips Hue-Lampe basierend auf Kalenderereignissen zu steuern. Die Lampe zeigt eine Farbe, die mit bestimmten Ereignistiteln im Kalender verknüpft ist. Wenn mehrere Ereignisse gleichzeitig aktiv sind, wechselt die Lampe sanft zwischen den zugehörigen Farben.

Ich nutze dieses Projekt als Docker Container auf meinem Raspberry Pi, um mich an Müllabholungen zu erinnern. Dafür trage ich für jeden Abholungstag die entsprechenden Ereignisse in meinen Kalender ein. Am Abend vor einer geplanten Abholung zeigt die Lampe automatisch die definierte Farbe für den Abfalltyp (z. B. Gelb für Plastikmüll, Grün für Bioabfall, Blau für Papier). Dadurch vergesse ich nicht mehr, die Mülltonnen rechtzeitig rauszustellen, und profitiere von einer automatisierten und praktischen Lösung im Alltag.

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
- Philips Hue Bridge und eine Philips Hue-Lampe (Color).

### Bibliotheken
- `phue` – Für die Steuerung der Philips Hue-Lampen.
- `caldav` – Für den Zugriff auf CalDAV-kompatible Kalender.
- `python-dotenv` – Zum Laden von Umgebungsvariablen aus einer `.env`-Datei.
- `pytz` – Zum Einstellen der lokalen Zeit.

## .env Datei Konfiguration

Die `.env`-Datei enthält alle wichtigen Konfigurationsparameter für das Projekt.

### Beispiel `.env`-Datei

```dotenv
HUE_BRIDGE_IP=192.168.x.x
LIGHT_NAME=ExampleLight
BRIGHTNESS=150

CALDAV_URL=https://caldav.example.com
CALDAV_USERNAME=example_user@example.com
CALDAV_PASSWORD=example_password
CALENDAR_NAME=ExampleCalendar
CALENDAR_CHECK_INTERVAL=10
OFFSET=12

TITLE_COLOR_MAPPING='{
    "Biotonne": [0,255,0],
    "Restmülltonne": [255,0,0],
    "Altpapier": [0,0,255],
    "Gelbe Säcke": [255,255,0]
    }'
TZ=Europe/Berlin
LOG_LEVEL=INFO
```

### Variablenbeschreibung

| Variable                  | Beschreibung                                | Beispielwert                 |
|---------------------------|---------------------------------------------|------------------------------|
| `HUE_BRIDGE_IP`           | IP-Adresse Ihrer Philips Hue-Bridge         | `192.168.x.x`                |
| `LIGHT_NAME`              | Name der Lampe, die gesteuert wird          | `ExampleLight`               |
| `BRIGHTNESS`              | Helligkeit der Lampe (0–254)                | `150`                        |
| `CALDAV_URL`              | URL Ihres CalDAV-kompatiblen Kalenders      | `https://caldav.example.com` |
| `CALDAV_USERNAME`         | Benutzername für den Kalender               | `example_user@example.com`   |
| `CALDAV_PASSWORD`         | Passwort für den Kalender                   | `example_password`           |
| `CALENDAR_NAME`           | Name des Kalenders                          | `ExampleCalendar`            |
| `CALENDAR_CHECK_INTERVAL` | Prüfintervall in Minuten                    | `10`                         |
| `OFFSET`                  | Zeitlicher Abstand vor dem Ereignis in Std  | `12`                         |
| `TITLE_COLOR_MAPPING`     | JSON-Zuordnung von Ereignistiteln zu Farben | Siehe `.env`-Beispiel.       |
| `TZ`                      | Zeitzone für die lokale Zeit                | `Europe/Berlin`              |
| `LOG_LEVEL`               | Log-Level (DEBUG, INFO, WARNING, ERROR)     | `INFO`                       |

---

### Docker Nutzung

#### Mit Docker Compose

1. **Image erstellen:**
   ```bash
   docker compose build
   ```                
2. **.env-Datei verwenden:**
Stelle sicher, dass die .env-Datei im selben Verzeichnis wie die compose.yaml liegt.
3. **Container starten:**
   ```bash
   docker compose up -d
   ```


#### Mit Docker Pull und .env-Datei
1. **Image von Docker Hub ziehen:**
   ```bash
   docker pull twoaace/trash-alert
   ```
2. **.env-Datei erstellen**
3. **Container starten:**
   ```bash
   docker run --env-file .env twoaace/trash-alert
   ```   