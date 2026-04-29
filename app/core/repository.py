"""
Patrón Repository: Abstracción para acceso a datos.

Define interfaces y implementaciones de repositorio para persistencia.
Principios aplicados:
- Dependency Inversion Principle: Dependemos de abstracciones, no de implementaciones.
- Single Responsibility: Solo gestiona acceso a datos.
"""

from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")

class Repository(ABC, Generic[T]):
    """Interfaz abstracta para repositorios genéricos asíncronos."""

    @abstractmethod
    async def add(self, entity: T) -> T:
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
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

class InMemoryRepository(Repository[T]):
    """Implementación de repositorio en memoria (Asíncrono)."""

    def __init__(self) -> None:
        self._data: Dict[str, T] = {}

    async def add(self, entity: T) -> T:
        self._data[str(entity.id)] = entity
        return entity

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        return self._data.get(entity_id)

    async def get_all(self) -> List[T]:
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