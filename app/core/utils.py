"""
Utilidades generales de la aplicación.

Módulo para funciones auxiliares y utilidades comunes reutilizables.
"""

from functools import wraps
from logging import getLogger
from typing import Any, Callable, TypeVar

logger = getLogger(__name__)

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
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"{func.__name__} returned {result}")
        return result

    return wrapper
