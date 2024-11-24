from dotenv import load_dotenv
import os

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()


class Config:
    HUE_BRIDGE_IP = os.getenv("HUE_BRIDGE_IP")
    CALDAV_URL = os.getenv("CALDAV_URL")
    CALDAV_USERNAME = os.getenv("CALDAV_USERNAME")
    CALDAV_PASSWORD = os.getenv("CALDAV_PASSWORD")
    LIGHT_NAME = os.getenv("LIGHT_NAME")
    LOG_LEVEL = os.getenv("LOG_LEVEL")
    CALENDAR_NAME = os.getenv("CALENDAR_NAME")


config = Config()
