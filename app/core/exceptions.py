"""
Excepciones personalizadas de la aplicación.

Define excepciones específicas del dominio para un manejo de errores
consistente en toda la aplicación.

Principios aplicados:
- Fail-fast: Excepciones específicas para cada error.
- Single Responsibility: Cada excepción representa un error único.
"""


class AppException(Exception):
    """Excepción base de la aplicación."""

    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR") -> None:
        """
        Inicializa la excepción.

        Args:
            message: Mensaje de error descriptivo.
            error_code: Código de error para categorización.
        """
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class ValidationException(AppException):
    """Se lanza cuando los datos de entrada son inválidos."""

    def __init__(self, message: str) -> None:
        """Inicializa la excepción de validación."""
        super().__init__(message, "VALIDATION_ERROR")


class ResourceNotFoundException(AppException):
    """Se lanza cuando un recurso no se encuentra."""

    def __init__(self, resource: str, resource_id: str) -> None:
        """Inicializa la excepción de recurso no encontrado."""
        message = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(message, "RESOURCE_NOT_FOUND")


class DuplicateResourceException(AppException):
    """Se lanza cuando se intenta crear un recurso duplicado."""

    def __init__(self, resource: str, identifier: str) -> None:
        """Inicializa la excepción de recurso duplicado."""
        message = f"{resource} con {identifier} ya existe"
        super().__init__(message, "DUPLICATE_RESOURCE")


class BusinessLogicException(AppException):
    """Se lanza cuando se viola una regla de negocio."""

    def __init__(self, message: str) -> None:
        """Inicializa la excepción de lógica de negocio."""
        super().__init__(message, "BUSINESS_LOGIC_ERROR")
