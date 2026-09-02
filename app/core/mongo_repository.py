from typing import Generic, TypeVar

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.repository import Repository

T = TypeVar("T")


class MongoRepository(Repository[T], Generic[T]):
    """Repo MongoDB asíncrono con Motor."""

    def __init__(
        self, db: AsyncIOMotorDatabase, collection_name: str, entity_class: type[T]
    ):
        self.collection = db[collection_name]
        self.entity_class = entity_class

    async def add(self, entity: T) -> T:
        await self.collection.insert_one(self._to_document(entity))
        return entity

    async def get_by_id(self, entity_id: str) -> T | None:
        document = await self.collection.find_one({"_id": entity_id})
        if document:
            return self._to_entity(document)
        return None

    async def get_all(self) -> list[T]:
        entities = []
        async for document in self.collection.find():
            entities.append(self._to_entity(document))
        return entities

    async def update(self, entity: T) -> T:
        await self.collection.replace_one({"_id": entity.id}, self._to_document(entity))
        return entity

    async def delete(self, entity_id: str) -> bool:
        result = await self.collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def find_one(self, filters: dict) -> T | None:
        document = await self.collection.find_one(filters)
        if document:
            return self._to_entity(document)
        return None

    def _to_document(self, entity: T) -> dict:
        """Entidad de dominio -> documento Mongo (id -> _id)."""
        document = entity.__dict__.copy()
        document["_id"] = document.pop("id")
        return document

    def _to_entity(self, document: dict) -> T:
        """Documento Mongo -> instancia de entidad (_id -> id)."""
        document["id"] = document.pop("_id")
        return self.entity_class(**document)
