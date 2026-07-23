"""
Utilidades generales de la aplicación.

Módulo para funciones auxiliares y utilidades comunes reutilizables.
"""

import logging
import sys
from functools import wraps
from typing import Any, Callable, TypeVar
from app.core.config import settings

# 1. Configuramos el formato estándar de los logs para toda la aplicación
logging.basicConfig(
    stream=sys.stdout,
    level=settings.log_level.upper(), # Toma el nivel de tu .env
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 2. Creamos la instancia principal que usarás en toda la app
# Reemplazamos getLogger(__name__) para que use el nombre de tu app del .env
logger = logging.getLogger(settings.app_name)

T = TypeVar("T")

def log_function_call(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorador para registrar llamadas a funciones con logging.

    Args:
        func: La función a decorar.

    Returns:
        La función decorada con logging.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        # Ahora este logger utilizará la configuración global que definimos arriba
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} returned {result}")
        return result

    return wrapper