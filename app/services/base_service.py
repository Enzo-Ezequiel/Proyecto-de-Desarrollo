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
    Servicio base genérico que proporciona operaciones CRUD comunes (Asíncrono).

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

    async def create(self, entity: T) -> T:
        """
        Crea una nueva entidad.
        """
        return await self._repository.add(entity)

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.
        """
        return await self._repository.get_by_id(entity_id)

    async def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.
        """
        return await self._repository.get_all()

    async def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.
        """
        # ⚠️ Cambio importante: ¡Ahora debemos usar await para verificar si existe!
        existing_entity = await self._repository.get_by_id(str(entity.id))
        if existing_entity is None:
            raise ResourceNotFoundException("Entidad", str(entity.id))

        return await self._repository.update(entity)

    async def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad.
        """
        return await self._repository.delete(entity_id)

    async def count(self) -> int:
        """
        Cuenta el número total de entidades.
        """
        return await self._repository.count()