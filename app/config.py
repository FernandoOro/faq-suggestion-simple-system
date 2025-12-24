"""
Configuración centralizada de la aplicación.
"""
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INITIAL_KNOWLEDGE_FILE = DATA_DIR / "initial_knowledge.json"

APP_NAME = "FAQ Suggestion API"
APP_VERSION = "1.0.0"
API_PREFIX = "/api/v1"

LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging():
    """Configura el sistema de logging de la aplicación."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(APP_NAME)


logger = setup_logging()
