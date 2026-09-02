"""Servicio base genérico con CRUD asíncrono usando patrón Repository."""

from typing import Generic, TypeVar

from app.core.exceptions import ResourceNotFoundException
from app.core.repository import InMemoryRepository, Repository

T = TypeVar("T")


class BaseService(Generic[T]):
    """CRUD genérico asíncrono. Tipo T = entidad que maneja el servicio."""

    def __init__(self, repository: Repository[T] | None = None) -> None:
        """Inicializa con repo dado o InMemoryRepository por defecto."""
        self._repository: Repository[T] = repository or InMemoryRepository[T]()

    async def create(self, entity: T) -> T:
        """Crea entidad nueva."""
        return await self._repository.add(entity)

    async def get_by_id(self, entity_id: str) -> T | None:
        """Obtiene entidad por ID."""
        return await self._repository.get_by_id(entity_id)

    async def get_all(self) -> list[T]:
        """Lista todas las entidades."""
        return await self._repository.get_all()

    async def update(self, entity: T) -> T:
        """Actualiza entidad existente (lanza si no existe)."""
        existing = await self._repository.get_by_id(str(entity.id))
        if existing is None:
            raise ResourceNotFoundException("Entidad", str(entity.id))
        return await self._repository.update(entity)

    async def delete(self, entity_id: str) -> bool:
        """Elimina entidad por ID."""
        return await self._repository.delete(entity_id)
