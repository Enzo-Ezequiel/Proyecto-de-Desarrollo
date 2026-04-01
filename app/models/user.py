"""
Modelo de Usuario: Entidad de dominio que representa un usuario en el sistema.

Principios aplicados:
- Single Responsibility: Esta clase solo representa la estructura de un usuario.
- Encapsulación: Los atributos están bien definidos y documentados.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.core.exceptions import ValidationException

from .base_model import BaseEntity


class User(BaseEntity):
    """
    Representa un usuario en el sistema.

    Atributos:
        email: Correo electrónico único del usuario.
        full_name: Nombre completo del usuario.
        is_active: Indica si el usuario está activo.
        description: Descripción o biografía del usuario (opcional).
    """

    @staticmethod
    def _validate_email(email: str) -> None:
        """
        Valida el formato del correo electrónico.

        Args:
            email: El correo a validar.

        Raises:
            ValidationException: Si el email es inválido.
        """
        if not email or "@" not in email:
            raise ValidationException("Email inválido")

    @staticmethod
    def _validate_full_name(full_name: str) -> None:
        """
        Valida el nombre completo del usuario.

        Args:
            full_name: El nombre a validar.

        Raises:
            ValidationException: Si el nombre es demasiado corto.
        """
        if len(full_name) < 2:
            raise ValidationException("El nombre debe tener al menos 2 caracteres")

    def __init__(
        self,
        email: str,
        full_name: str,
        is_active: bool = True,
        description: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Inicializa un nuevo usuario.

        Args:
            email: Correo electrónico del usuario.
            full_name: Nombre completo del usuario.
            is_active: Si el usuario está activo (por defecto True).
            description: Descripción del usuario (opcional).
            id: ID único (generado automáticamente si no se proporciona).
            created_at: Marca de tiempo de creación.
            updated_at: Marca de tiempo de actualización.

        Raises:
            ValidationException: Si el email está vacío o el nombre es demasiado corto.
        """
        # Validar datos antes de inicializar
        self._validate_email(email)
        self._validate_full_name(full_name)

        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.email: str = email
        self.full_name: str = full_name
        self.is_active: bool = is_active
        self.description: Optional[str] = description

    def deactivate(self) -> None:
        """Desactiva el usuario."""
        self.is_active = False
        self.update_timestamp()

    def activate(self) -> None:
        """Activa el usuario."""
        self.is_active = True
        self.update_timestamp()

    def update_profile(
        self,
        full_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Actualiza el perfil del usuario.

        Args:
            full_name: Nuevo nombre completo (si se proporciona).
            description: Nueva descripción (si se proporciona).

        Raises:
            ValidationException: Si el nombre es demasiado corto.
        """
        if full_name is not None:
            self._validate_full_name(full_name)
            self.full_name = full_name

        if description is not None:
            self.description = description

        self.update_timestamp()

    def __repr__(self) -> str:
        """Representación legible del usuario."""
        return f"User(id={self.id}, email={self.email}, name={self.full_name})"
