import time
import pytz
from itertools import cycle
from datetime import datetime, timedelta
from utils import config, fetch_calendar_events, map_title_to_color, HueBridgeConnection, logger


def main():
    # Verbinde mit Philips Hue
    hue_connection = HueBridgeConnection(config.HUE_BRIDGE_IP)

    while True:
        iteration_start_time = time.time()
        try:
            # Aktuelle Zeit
            local_tz = pytz.timezone(config.TZ)
            datetime_now = datetime.now(local_tz)

            # Lade Kalenderereignisse
            events = fetch_calendar_events(
                config.CALDAV_URL,
                config.CALDAV_USERNAME,
                config.CALDAV_PASSWORD,
                config.CALENDAR_NAME,
                datetime_now
            )

            # Ereignis prüfen, ob es im gewünschten Zeitfenster liegt
            active_colors = []
            for event in events:
                # Parse des Ereignisses in ein Python-Datetime-Objekt
                event_title = event.get("title")
                start_time = event.get("start")
                end_time = event.get("end")

                # Überspringen, wenn Zeiten fehlen
                if not start_time or not end_time:
                    logger.warn("Keine Start und/oder Endzeit im Ereignis! Überspringe zum nächsten Ereignis...")
                    continue

                # Zeitfenster: X Stunden vor Start bis Ende des Ereignisses
                light_start = start_time - timedelta(hours=config.OFFSET)
                light_end = end_time - timedelta(hours=config.OFFSET)

                # Prüfen, ob die aktuelle Zeit im Zeitfenster liegt
                if light_start <= datetime_now <= light_end:
                    color = map_title_to_color(event_title, config.TITLE_COLOR_MAPPING)
                    active_colors.append(color)

            if active_colors:
                logger.info(f"Aktive Farben: {active_colors}")

                if len(active_colors) == 1:
                    # Nur eine Farbe
                    hue_connection.set_hue_color(config.LIGHT_NAME, active_colors[0], config.BRIGHTNESS)
                else:
                    logger.info(f"Mehrere Farben: Cycle-Modus.")
                    color_cycle = cycle(active_colors)
                    current_color = next(color_cycle)

                    # Leuchtet für die nächsten 5 Minuten
                    for _ in range(60):
                        next_color = next(color_cycle)
                        hue_connection.transition_lights(
                            light_name=config.LIGHT_NAME,
                            start_color=current_color,
                            end_color=next_color,
                            steps=20,
                            transition_time=0.10,
                            stay_time=5
                        )
                        current_color = next_color
            else:
                # Wenn kein relevantes Ereignis gefunden wurde, schalte die Lampe aus
                hue_connection.set_hue_color(config.LIGHT_NAME, None, config.BRIGHTNESS)  # Lampe ausschalten
                logger.info("Kein passendes Ereignis gefunden. Lampe ausgeschaltet.")

        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten der Ereignisse: {e}")

        # Warte bis zur nächsten Abfrage
        elapsed_time = time.time() - iteration_start_time
        sleep_time = max(0, (config.CALENDAR_CHECK_INTERVAL * 60) - elapsed_time)
        # Minuten und Sekunden berechnen
        sleep_minutes = int(sleep_time // 60)
        sleep_seconds = int(sleep_time % 60)
        logger.info(f"Warte bis zur nächsten Kalender Abfrage: {sleep_minutes} Minuten und {sleep_seconds} Sekunden.")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
