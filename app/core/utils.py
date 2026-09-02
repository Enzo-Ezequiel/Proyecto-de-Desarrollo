"""Utilidades comunes: logger."""

import logging
import sys

from app.core.config import settings

# Logger root en WARNING para que librerías de terceros no inunden stdout
logging.basicConfig(
    stream=sys.stdout,
    level=logging.WARNING,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Logger principal de la app (nivel desde .env)
logger = logging.getLogger(settings.app_name)
logger.setLevel(settings.log_level.upper())
