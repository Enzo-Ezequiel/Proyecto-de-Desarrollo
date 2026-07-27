"""Utilidades comunes: logger y decoradores."""

import logging
import sys
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

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

T = TypeVar("T")


def log_function_call(func: Callable[..., T]) -> Callable[..., T]:
    """Decorador que loggea entrada y salida de función."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        logger.debug(f"Calling {func.__name__} args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} returned {result}")
        return result

    return wrapper
