from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.utils import logger

client: AsyncIOMotorClient = None
db = None


async def connect_to_mongo():
    """Abre conexión a MongoDB."""
    global client, db
    try:
        client = AsyncIOMotorClient(settings.database_url)
        db = client[settings.mongo_db_name]
        logger.info("Conectado a MongoDB")
    except Exception as e:
        logger.error(f"Fallo crítico conectando a MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Cierra conexión a MongoDB."""
    if client is not None:
        client.close()
        logger.info("Conexión a MongoDB cerrada")


def get_database():
    """Devuelve instancia de la base de datos."""
    return db
