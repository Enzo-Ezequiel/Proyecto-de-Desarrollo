"""
Servicio Base: Clase base para todos los servicios de la aplicación.

Proporciona métodos comunes y patrones de acceso a datos.
Principios aplicados:
- Template Method Pattern: Define la estructura general de los servicios.
- Dependency Inversion: Los servicios usan abstracciones, no implementaciones concretas.
"""

from typing import Generic, List, Optional, TypeVar

from app.core.exceptions import ResourceNotFoundException
from app.core.repository import InMemoryRepository, Repository

T = TypeVar("T")  # Type variable para genéricos


class BaseService(Generic[T]):
    """
    Servicio base genérico que proporciona operaciones CRUD comunes.

    Tipo genérico T: El tipo de entidad que maneja el servicio.
    Usa el patrón Repository para abstraer el acceso a datos.
    """

    def __init__(self, repository: Optional[Repository[T]] = None) -> None:
        """
        Inicializa el servicio con un repositorio.

        Args:
            repository: Repositorio a usar. Si no se proporciona, usa InMemoryRepository.
        """
        self._repository: Repository[T] = repository or InMemoryRepository[T]()

    def create(self, entity: T) -> T:
        """
        Crea una nueva entidad.

        Args:
            entity: La entidad a crear.

        Returns:
            La entidad creada.
        """
        return self._repository.add(entity)

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.

        Args:
            entity_id: El ID de la entidad.

        Returns:
            La entidad si existe, None en caso contrario.
        """
        return self._repository.get_by_id(entity_id)

    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.

        Returns:
            Lista de todas las entidades.
        """
        return self._repository.get_all()

    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.

        Args:
            entity: La entidad a actualizar.

        Returns:
            La entidad actualizada.

        Raises:
            ResourceNotFoundException: Si la entidad no existe.
        """
        if self._repository.get_by_id(str(entity.id)) is None:
            raise ResourceNotFoundException("Entidad", str(entity.id))

        return self._repository.update(entity)

    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad.

        Args:
            entity_id: El ID de la entidad a eliminar.

        Returns:
            True si la entidad fue eliminada, False si no existía.
        """
        return self._repository.delete(entity_id)

    def count(self) -> int:
        """
        Cuenta el número total de entidades.

        Returns:
            Número de entidades en el repositorio.
        """
        return self._repository.count()
