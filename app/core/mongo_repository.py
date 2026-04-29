"""
Repositorio MongoDB.

Implementación de Repository usando MongoDB con motor.
Principios aplicados:
- Dependency Inversion: Implementa la abstracción Repository.
- Single Responsibility: Solo gestiona acceso a datos MongoDB.
"""

import json
from typing import Dict, Generic, List, Optional, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection

from app.core.repository import Repository
from app.models.base_model import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class MongoEncoder(json.JSONEncoder):
    """Codificador JSON para entidades."""

    def default(self, obj):
        if isinstance(obj, BaseEntity):
            return obj.__dict__
        return super().default(obj)


class MongoRepository(Repository[T]):
    """
    Implementación de repositorio para MongoDB.

    Usa una colección MongoDB para persistir entidades.
    """

    def __init__(
        self, collection: AsyncIOMotorCollection, model_class: type[T]
    ) -> None:
        """
        Inicializa el repositorio.

        Args:
            collection: Colección MongoDB.
            model_class: Clase del modelo.
        """
        self._collection = collection
        self._model_class = model_class
        self._encoder = MongoEncoder()

    def _entity_to_dict(self, entity: T) -> Dict:
        """Convierte una entidad a diccionario."""
        return {"_id": str(entity.id), **entity.__dict__}

    def _dict_to_entity(self, data: Dict) -> T:
        """Convierte un diccionario a entidad."""
        if "_id" in data:
            data.pop("_id")
        return self._model_class(**data)

    def add(self, entity: T) -> T:
        """
        Agrega una entidad al repositorio.

        Args:
            entity: La entidad a agregar.

        Returns:
            La entidad agregada.
        """
        data = self._entity_to_dict(entity)
        self._collection.insert_one(data)
        return entity

    def get_by_id(self, entity_id: str) -> Optional[T]:
        """
        Obtiene una entidad por su ID.

        Args:
            entity_id: El ID de la entidad.

        Returns:
            La entidad si existe, None en caso contrario.
        """
        data = self._collection.find_one({"_id": entity_id})
        if data is None:
            return None
        return self._dict_to_entity(data)

    def get_all(self) -> List[T]:
        """
        Obtiene todas las entidades.

        Returns:
            Lista de todas las entidades.
        """
        entities = []
        for data in self._collection.find():
            entities.append(self._dict_to_entity(data))
        return entities

    def update(self, entity: T) -> T:
        """
        Actualiza una entidad existente.

        Args:
            entity: La entidad a actualizar.

        Returns:
            La entidad actualizada.
        """
        data = self._entity_to_dict(entity)
        self._collection.replace_one({"_id": str(entity.id)}, data)
        return entity

    def delete(self, entity_id: str) -> bool:
        """
        Elimina una entidad.

        Args:
            entity_id: El ID de la entidad a eliminar.

        Returns:
            True si la entidad fue eliminada, False si no existía.
        """
        result = self._collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    def count(self) -> int:
        """
        Cuenta el número de entidades.

        Returns:
            Número de entidades en el repositorio.
        """
        return self._collection.count_documents({})
