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
        document = entity.__dict__.copy()
        document["_id"] = document.pop("id")
        await self.collection.insert_one(document)
        return entity

    async def get_by_id(self, entity_id: str) -> T | None:
        document = await self.collection.find_one({"_id": entity_id})
        if document:
            document["id"] = document.pop("_id")
            return self.entity_class(**document)
        return None

    async def get_all(self) -> list[T]:
        entities = []
        async for document in self.collection.find():
            document["id"] = document.pop("_id")
            entities.append(self.entity_class(**document))
        return entities

    async def update(self, entity: T) -> T:
        document = entity.__dict__.copy()
        document["_id"] = document.pop("id")
        await self.collection.replace_one({"_id": entity.id}, document)
        return entity

    async def delete(self, entity_id: str) -> bool:
        result = await self.collection.delete_one({"_id": entity_id})
        return result.deleted_count > 0

    async def count(self) -> int:
        return await self.collection.count_documents({})

    async def find_one(self, filters: dict) -> T | None:
        document = await self.collection.find_one(filters)
        if document:
            document["id"] = document.pop("_id")
            return self.entity_class(**document)
        return None
