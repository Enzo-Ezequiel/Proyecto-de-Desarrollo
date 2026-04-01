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
    """
    Interfaz abstracta para repositorios genéricos.

    Define los métodos que todo repositorio debe implementar.
    """

    @abstractmethod
    def add(self, entity: T) -> T:
        """Agrega una entidad al repositorio."""
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza una entidad."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Elimina una entidad."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Cuenta el número de entidades."""
        pass


class InMemoryRepository(Repository[T]):
    """
    Implementación de repositorio en memoria.

    Útil para desarrollo, testing y aplicaciones sin persistencia.
    """

    def __init__(self) -> None:
        """Inicializa el repositorio en memoria."""
        self._data: Dict[str, T] = {}

    def add(self, entity: T) -> T:
        """
        Agrega una entidad al repositorio.

        Args:
            entity: La entidad a agregar.

        Returns:
            La entidad agregada.
        """
        self._data[str(entity.id)] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.

        Args:
            entity_id: El ID de la entidad.

        Returns:
            La entidad si existe, None en caso contrario.
        """
        return self._data.get(entity_id)

    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.

        Returns:
            Lista de todas las entidades.
        """
        return list(self._data.values())

    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.

        Args:
            entity: La entidad a actualizar.

        Returns:
            La entidad actualizada.
        """
        self._data[str(entity.id)] = entity
        return entity

    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad.

        Args:
            entity_id: El ID de la entidad a eliminar.

        Returns:
            True si la entidad fue eliminada, False si no existía.
        """
        if entity_id in self._data:
            del self._data[entity_id]
            return True
        return False

    def count(self) -> int:
        """
        Cuenta el número de entidades.

        Returns:
            Número de entidades en el repositorio.
        """
        return len(self._data)
