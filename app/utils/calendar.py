from datetime import datetime, timedelta
from caldav import DAVClient
from .logging import logger


def fetch_calendar_events(client_url, username, password, calendar_name, datetime_now):
    try:
        logger.info("Verbindung zum CalDAV-Server wird hergestellt...")
        client = DAVClient(client_url, username=username, password=password)

        # Principal abrufen
        principal = client.principal()
        calendars = principal.calendars()
        if not calendars:
            logger.warning("Keine Kalender gefunden.")
            return []

        # Wenn ein Kalendername angegeben ist, diesen suchen
        if calendar_name:
            logger.info(f"Suche nach dem Kalender: '{calendar_name}'...")
            calendar = next((cal for cal in calendars if cal.name == calendar_name), None)
            if not calendar:
                logger.warning(f"Kalender mit dem Namen '{calendar_name}' wurde nicht gefunden.")
                return []
            logger.info(f"Gefundener Kalender: {calendar.name}")
        else:
            # Standardmäßig den ersten Kalender verwenden
            calendar = calendars[0]
            logger.info(f"Kein Kalendername angegeben. Standardmäßig wird '{calendar.name}' verwendet.")

        # Zeitbereich für die Abfrage
        start = datetime_now
        end = start + timedelta(days=1)
        logger.info(f"Ereignisse werden für den Zeitraum {start} bis {end} abgerufen...")

        # Ereignisse abrufen
        events = calendar.date_search(start=start, end=end)
        event_details = []

        for event in events:
            try:
                vevent = event.vobject_instance.vevent
                title = vevent.summary.value
                start_time = vevent.dtstart.value
                end_time = vevent.dtend.value if hasattr(vevent, 'dtend') else None

                event_details.append({
                    "title": title,
                    "start": start_time,
                    "end": end_time
                })
            except Exception as e:
                logger.error(f"Fehler beim Verarbeiten eines Ereignisses: {e}")

        logger.info(f"{len(event_details)} Ereignis(se) gefunden.")
        logger.info(f"{event_details}")
        return event_details

    except Exception as e:
        logger.error(f"Ein unbekannter Fehler ist aufgetreten: {e}")
        return []
