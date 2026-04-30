"""
Modelo Base: Clase base para todas las entidades del dominio.

Este módulo proporciona la clase base que todas las entidades de negocio
deben extender. Sigue el principio DRY y permite reutilizar atributos
comunes como timestamps y identificadores.

Principios aplicados:
- DRY: Evita duplicación de código
- Single Responsibility: Solo gestiona la representación base de entidades
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4


class BaseEntity:
    """
    Clase base para todas las entidades del dominio.

    Atributos:
        id: Identificador único de la entidad (String).
        created_at: Fecha y hora de creación de la entidad.
        updated_at: Fecha y hora de la última actualización.
    """

    def __init__(
        self,
        id: Optional[str] = None,  # Cambiamos UUID por str
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """
        Inicializa una nueva entidad.

        Args:
            id: ID único de la entidad. Si no se proporciona, se genera uno nuevo en string.
            created_at: Marca de tiempo de creación. Si no se proporciona, usa la actual.
            updated_at: Marca de tiempo de actualización. Si no se proporciona, usa la actual.
        """
        # Convertimos el UUID generado a texto, o guardamos el string que venga de MongoDB
        self.id: str = str(id) if id else str(uuid4())
        self.created_at: datetime = created_at or datetime.now(timezone.utc)
        self.updated_at: datetime = updated_at or datetime.now(timezone.utc)

    def update_timestamp(self) -> None:
        """Actualiza la marca de tiempo de la última modificación."""
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other: object) -> bool:
        """Compara dos entidades por su ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Permite usar entidades en sets y como claves de diccionarios."""
        return hash(self.id)

    def __repr__(self) -> str:
        """Representación legible de la entidad."""
        return f"{self.__class__.__name__}(id={self.id})"