from phue import Bridge
import time
from .logging import logger
import json


def rgb_to_xy(rgb_color):
    r, g, b = [x / 255.0 for x in rgb_color]
    r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4

    x = r * 0.649926 + g * 0.103455 + b * 0.197109
    y = r * 0.234327 + g * 0.743075 + b * 0.022598
    z = r * 0.000000 + g * 0.053077 + b * 1.035763

    if x + y + z == 0:
        return 0.0, 0.0

    return x / (x + y + z), y / (x + y + z)


def map_title_to_color(event_title):
    mapping = {
        "Biotonne": (0, 255, 0),
        "Restmülltonne": (255, 0, 0),
        "Altpapier": (0, 0, 255),
        "Gelbe Säcke": (255, 255, 0)
    }
    return mapping.get(event_title, (255, 255, 255))


class HueBridgeConnection:
    """
    Klasse zur Verwaltung der Verbindung zur Hue-Bridge.
    Stellt sicher, dass nur eine Verbindung existiert und wiederverwendet wird.
    """
    CONFIG_FILE = "hue_connection.json"

    def __init__(self, bridge_ip):
        """
        Initialisiert die Verbindung zur Hue Bridge.
        :param bridge_ip: Die IP-Adresse der Hue-Bridge
        """
        self.bridge_ip = bridge_ip
        self.bridge = None

    def save_connection(self, username):
        """
        Speichert die Verbindung in einer JSON-Datei.
        :param username: Der generierte Benutzername der Bridge
        """
        config_data = {"bridge_ip": self.bridge_ip, "username": username}
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(config_data, f)
        logger.info(f"Verbindung gespeichert in {self.CONFIG_FILE}")

    def load_connection(self):
        """
        Lädt die gespeicherte Verbindung aus der JSON-Datei.
        :return: True, wenn die Verbindung geladen wurde, sonst False.
        """
        try:
            with open(self.CONFIG_FILE, "r") as f:
                config_data = json.load(f)
                if config_data["bridge_ip"] == self.bridge_ip:
                    self.bridge = Bridge(self.bridge_ip, username=config_data["username"])
                    logger.info("Gespeicherte Verbindung erfolgreich geladen.")
                    return True
        except FileNotFoundError:
            logger.info(f"Keine gespeicherte Verbindung gefunden in {self.CONFIG_FILE}")
        except Exception as e:
            logger.error(f"Fehler beim Laden der Verbindung: {e}")
        return False

    def connect(self):
        """
        Stellt die Verbindung zur Bridge her, entweder durch Laden oder durch eine neue Authentifizierung.
        """
        if not self.load_connection():
            while True:
                try:
                    logger.info(f"Versuche, eine Verbindung zur Hue Bridge ({self.bridge_ip}) herzustellen...")
                    self.bridge = Bridge(self.bridge_ip)
                    self.bridge.connect()  # Authentifiziert sich mit der Bridge
                    logger.info("Erfolgreich mit der Hue Bridge verbunden!")
                    self.save_connection(self.bridge.username)
                    break
                except Exception as e:
                    logger.error(f"Verbindung fehlgeschlagen: {e}")
                    logger.info("Bitte den Knopf auf der Hue Bridge drücken und erneut versuchen.")
                    time.sleep(10)

    def get_bridge(self):
        """
        Gibt die verbundene Bridge zurück.
        :return: Bridge-Objekt
        """
        if not self.bridge:
            self.connect()
        return self.bridge

    def set_hue_color(self, light_name, rgb_color):
        """
        Setzt die Farbe einer Hue-Lampe auf eine RGB-Farbe.

        :param light_name: Name der Lampe, die gesteuert werden soll
        :param rgb_color: Tuple (R, G, B) mit Farbwerten (0–255)
        """
        try:
            # Verbindung zur Bridge abrufen
            bridge = self.get_bridge()

            # Prüfen, ob die Lampe existiert
            lights = bridge.get_light_objects('name')
            if light_name not in lights:
                raise ValueError(f"Die Lampe '{light_name}' wurde nicht gefunden.")

            light = lights[light_name]

            if rgb_color is None:
                # Lampe ausschalten
                light.on = False
                logger.info(f"Die Lampe '{light_name}' wurde ausgeschaltet.")
            else:
                # Lampe einschalten und Farbe setzen
                # Konvertiere RGB zu XY
                xy_color = rgb_to_xy(rgb_color)
                light.on = True
                light.xy = xy_color
                logger.info(f"Die Lampe '{light_name}' wurde auf die Farbe rgb={rgb_color} xy={xy_color} gesetzt.")

        except Exception as e:
            logger.error(f"Fehler beim Setzen der Farbe für die Lampe '{light_name}': {e}")

    def transition_lights(self, light_name, start_color, end_color, steps, transition_time, stay_time):
        """
        Führt einen sanften Übergang zwischen zwei Farben durch.
        :param light_name: Name der Lampe
        :param start_color: Startfarbe als (R, G, B)-Tupel
        :param end_color: Endfarbe als (R, G, B)-Tupel
        :param steps: Anzahl der Schritte für die Transition
        :param transition_time: Zeit zwischen den Schritten in Sekunden
        :param stay_time: Zeit in Sekunden wie lange die Farbe leuchten soll
        """
        try:
            bridge = self.get_bridge()
            lights = bridge.get_light_objects('name')
            if light_name not in lights:
                logger.error(f"Die Lampe '{light_name}' wurde nicht gefunden. Verfügbare Lampen: {list(lights.keys())}")
                return

            light = lights[light_name]

            for i in range(steps):
                # Interpoliere die Farben
                interpolated_color = tuple(
                    int(start_color[j] + (float(end_color[j] - start_color[j]) / steps) * i)
                    for j in range(3)
                )
                # Konvertiere interpolierte Farbe in XY
                xy_color = rgb_to_xy(interpolated_color)

                # Setze die Farbe mit Übergang
                light.xy = xy_color
                light.transitiontime = int(transition_time * 10)  # in 1/10 Sekunden
                time.sleep(transition_time)  # Warten, bis der Schritt abgeschlossen ist

            # Ziel-Farbe setzen konstant leuchten lassen
            light.xy = rgb_to_xy(end_color)
            light.transitiontime = 0  # Sofort setzen
            time.sleep(stay_time)

        except Exception as e:
            logger.error(f"Fehler bei der Transition für die Lampe '{light_name}': {e}")
