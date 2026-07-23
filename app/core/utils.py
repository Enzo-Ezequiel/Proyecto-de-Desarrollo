"""
Utilidades generales de la aplicación.

Módulo para funciones auxiliares y utilidades comunes reutilizables.
"""

import logging
import sys
from app.core.config import settings

logging.basicConfig(
    stream=sys.stdout,
    level=settings.log_level.upper(),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(settings.app_name)
