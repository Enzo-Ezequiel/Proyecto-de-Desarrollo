"""Patrón Repository: abstracción para acceso a datos.

Interfaces e implementaciones para persistencia.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Interfaz abstracta para repositorios genéricos asíncronos."""

    @abstractmethod
    async def add(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> T | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[T]:
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass

    @abstractmethod
    async def count(self) -> int:
        pass

    @abstractmethod
    async def find_one(self, filters: dict[str, Any]) -> T | None:
        """Busca primera entidad que coincida exactamente con filters."""
        pass


class InMemoryRepository(Repository[T]):
    """Repo en memoria (asíncrono)."""

    def __init__(self) -> None:
        self._data: dict[str, T] = {}

    async def add(self, entity: T) -> T:
        self._data[str(entity.id)] = entity
        return entity

    async def get_by_id(self, entity_id: str) -> T | None:
        return self._data.get(entity_id)

    async def get_all(self) -> list[T]:
        return list(self._data.values())

    async def update(self, entity: T) -> T:
        self._data[str(entity.id)] = entity
        return entity

    async def delete(self, entity_id: str) -> bool:
        if entity_id in self._data:
            del self._data[entity_id]
            return True
        return False

    async def count(self) -> int:
        return len(self._data)

    async def find_one(self, filters: dict[str, Any]) -> T | None:
        for entity in self._data.values():
            if all(
                getattr(entity, key, None) == value for key, value in filters.items()
            ):
                return entity
        return None
