import time
import pytz
from itertools import cycle
from datetime import datetime, timedelta
from utils import config, fetch_calendar_events, map_title_to_color, HueBridgeConnection, logger


def main():
    # Verbinde mit Philips Hue
    hue_connection = HueBridgeConnection(config.HUE_BRIDGE_IP)

    while True:
        already_waited = False
        try:
            # Lade Kalenderereignisse
            events = fetch_calendar_events(
                config.CALDAV_URL,
                config.CALDAV_USERNAME,
                config.CALDAV_PASSWORD,
                config.CALENDAR_NAME
            )

            # Aktuelle Zeit
            local_tz = pytz.timezone("Europe/Berlin")
            now = datetime.now(local_tz)

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

                # Zeitfenster: 12 Stunden vor Start bis Ende des Ereignisses
                light_start = start_time - timedelta(hours=12)
                light_end = end_time

                # Prüfen, ob die aktuelle Zeit im Zeitfenster liegt
                if light_start <= now <= light_end:
                    color = map_title_to_color(event_title)
                    active_colors.append(color)

            if active_colors:
                logger.info(f"Aktive Farben: {active_colors}")

                if len(active_colors) == 1:
                    # Nur eine Farbe
                    hue_connection.set_hue_color(config.LIGHT_NAME, active_colors[0])
                else:
                    logger.info(f"Mehrere Farben: Cycle-Modus.")
                    color_cycle = cycle(active_colors)
                    current_color = next(color_cycle)

                    # Leuchtet für die nächsten 5 Minuten
                    for _ in range(60):  # 60 * 5 Sekunden = 5 Minuten
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
                    already_waited = True
            else:
                # Wenn kein relevantes Ereignis gefunden wurde, schalte die Lampe aus
                hue_connection.set_hue_color(config.LIGHT_NAME, None)  # Lampe ausschalten
                logger.info("Kein passendes Ereignis gefunden. Lampe ausgeschaltet.")

        except Exception as e:
            logger.error(f"Fehler beim Verarbeiten der Ereignisse: {e}")

        if not already_waited:
            # Warte 5 Minuten bis zur nächsten Abfrage
            time.sleep(5 * 60)


if __name__ == "__main__":
    main()
