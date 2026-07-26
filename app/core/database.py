from motor.motor_asyncio import AsyncIOMotorClient
# Importamos settings desde tu archivo de configuración
from app.core.config import settings

# 1. Importamos nuestro logger
from app.core.utils import logger

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    """Abre la conexión con MongoDB"""
    try:
        db_instance.client = AsyncIOMotorClient(settings.database_url)
        db_instance.db = db_instance.client[settings.mongo_db_name]
        # 2. Reemplazamos el print por un mensaje de información
        logger.info("Conectado a MongoDB")
    except Exception as e:
        # 3. Registramos como ERROR CRÍTICO si la base de datos falla al conectar
        logger.error(f"Fallo crítico al intentar conectar a MongoDB: {e}")
        raise e

async def close_mongo_connection():
    """Cierra la conexión con MongoDB"""
    if db_instance.client is not None:
        db_instance.client.close()
        # 4. Reemplazamos el print del cierre
        logger.info("Conexión a MongoDB cerrada")

def get_database():
    """Devuelve la instancia de la base de datos"""
    return db_instance.db