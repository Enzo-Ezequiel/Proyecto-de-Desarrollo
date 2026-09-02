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

    def to_dict(self) -> dict:
        """Devuelve los atributos de instancia como dict.

        Incluye los de las subclases: `__dict__` es por instancia, así que una
        `DocumentoPDF` trae también `nombre_pdf`, `contenido_pdf` y `checksum`.
        La entidad decide qué expone; si algún campo necesitara transformarse al
        serializar, se resuelve acá, en un solo lugar.
        """
        return self.__dict__.copy()

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
