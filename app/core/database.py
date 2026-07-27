from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.utils import logger


class Database:
    client: AsyncIOMotorClient = None
    db = None


db_instance = Database()


async def connect_to_mongo():
    """Abre conexión a MongoDB."""
    try:
        db_instance.client = AsyncIOMotorClient(settings.database_url)
        db_instance.db = db_instance.client[settings.mongo_db_name]
        logger.info("Conectado a MongoDB")
    except Exception as e:
        logger.error(f"Fallo crítico conectando a MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cierra conexión a MongoDB."""
    if db_instance.client is not None:
        db_instance.client.close()
        logger.info("Conexión a MongoDB cerrada")


def get_database():
    """Devuelve instancia de la base de datos."""
    return db_instance.db
