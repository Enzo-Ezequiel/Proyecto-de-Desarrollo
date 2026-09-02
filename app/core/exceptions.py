"""Excepciones de dominio de la app."""


class AppException(Exception):
    """Excepción base."""

    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR") -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class ValidationException(AppException):
    """Datos de entrada inválidos."""

    def __init__(self, message: str) -> None:
        super().__init__(message, "VALIDATION_ERROR")


class ResourceNotFoundException(AppException):
    """Recurso no encontrado."""

    def __init__(self, resource: str, resource_id: str) -> None:
        message = f"{resource} con ID {resource_id} no encontrado"
        super().__init__(message, "RESOURCE_NOT_FOUND")


class DuplicateResourceException(AppException):
    """Recurso duplicado."""

    def __init__(self, resource: str, identifier: str) -> None:
        message = f"{resource} con {identifier} ya existe"
        super().__init__(message, "DUPLICATE_RESOURCE")
