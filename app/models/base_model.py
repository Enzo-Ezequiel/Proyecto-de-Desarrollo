"""
Clase base para entidades del dominio. ID, timestamps y métodos de comparación.
"""

from datetime import datetime, timezone
from uuid import uuid4


class BaseEntity:
    """Entidad base: trae ID único, created_at y updated_at automáticos."""

    def __init__(
        self,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Inicializa entidad. Genera ID y timestamps si no se pasan."""
        self.id: str = str(id) if id else str(uuid4())
        self.created_at: datetime = created_at or datetime.now(timezone.utc)
        self.updated_at: datetime = updated_at or datetime.now(timezone.utc)

    def update_timestamp(self) -> None:
        """Actualiza updated_at a ahora."""
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other: object) -> bool:
        """Compara por ID."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Para usar en sets y como keys de dict."""
        return hash(self.id)

    def __repr__(self) -> str:
        """Repr legible para debug."""
        return f"{self.__class__.__name__}(id={self.id})"
