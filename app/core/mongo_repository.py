from typing import Generic, List, Optional, Type, TypeVar
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.repository import Repository

T = TypeVar("T")

class MongoRepository(Repository[T], Generic[T]):
    """
    Implementación del repositorio para MongoDB usando Motor (asíncrono).
    """

    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str, entity_class: Type[T]):
        """
        Inicializa el repositorio.
        :param db: Instancia de la base de datos MongoDB.
        :param collection_name: Nombre de la colección (ej. 'usuarios').
        :param entity_class: Referencia a la clase de la entidad (ej. Usuario) para instanciarla.
        """
        self.collection = db[collection_name]
        self.entity_class = entity_class

    async def add(self, entity: T) -> T:
        document = entity.__dict__.copy()
        # MongoDB usa '_id' en lugar de 'id'. Hacemos el cambio:
        document["_id"] = document.pop("id")
        
        await self.collection.insert_one(document)
        return entity

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        document = await self.collection.find_one({"_id": entity_id})
        if document:
            # Revertimos '_id' a 'id' para que la entidad de dominio lo entienda
            document["id"] = document.pop("_id")
            return self.entity_class(**document)
        return None

    async def get_all(self) -> List[T]:
        entities = []
        # find() en motor devuelve un cursor asíncrono
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