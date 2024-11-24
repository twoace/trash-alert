import logging
from .config import config


def setup_logging():
    """Konfiguriert das Logging für die Anwendung."""
    log_level = config.LOG_LEVEL.upper()
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log", encoding="utf-8"),
        ]
    )
    return logging.getLogger("TrashAlert")


# Logger-Instanz erstellen
logger = setup_logging()
