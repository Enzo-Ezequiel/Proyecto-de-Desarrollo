"""
Excepciones personalizadas de la aplicación.

Define excepciones específicas del dominio para un manejo de errores
consistente en toda la aplicación.

Principios aplicados:
- Fail-fast: Excepciones específicas para cada error.
- Single Responsibility: Cada excepción representa un error único.
- OCP: Cada excepción conoce su status code HTTP (extensible sin modificar main.py).
"""

from http import HTTPStatus


class AppException(Exception):
    """Excepción base de la aplicación."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message: str) -> None:
        """
        Inicializa la excepción.

        Args:
            message: Mensaje de error descriptivo.
        """
        self.message = message
        super().__init__(message)


class ValidationException(AppException):
    """Se lanza cuando los datos de entrada son inválidos."""

    status_code = HTTPStatus.BAD_REQUEST
    error_code = "VALIDATION_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ResourceNotFoundException(AppException):
    """Se lanza cuando un recurso no se encuentra."""

    status_code = HTTPStatus.NOT_FOUND
    error_code = "RESOURCE_NOT_FOUND"

    def __init__(self, resource: str, resource_id: str) -> None:
        message = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(message)


class DuplicateResourceException(AppException):
    """Se lanza cuando se intenta crear un recurso duplicado."""

    status_code = HTTPStatus.BAD_REQUEST
    error_code = "DUPLICATE_RESOURCE"

    def __init__(self, resource: str, identifier: str) -> None:
        message = f"{resource} con {identifier} ya existe"
        super().__init__(message)


class BusinessLogicException(AppException):
    """Se lanza cuando se viola una regla de negocio."""

    status_code = HTTPStatus.BAD_REQUEST
    error_code = "BUSINESS_LOGIC_ERROR"

    def __init__(self, message: str) -> None:
        super().__init__(message)
