from motor.motor_asyncio import AsyncIOMotorClient
from app.core import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

db_instance = Database()

async def connect_to_mongo():
    """Abre la conexión con MongoDB"""
    db_instance.client = AsyncIOMotorClient(settings.database_url)
    db_instance.db = db_instance.client[settings.mongo_db_name]
    print("✅ Conectado a MongoDB")

async def close_mongo_connection():
    """Cierra la conexión con MongoDB"""
    if db_instance.client is not None:
        db_instance.client.close()
        print("🛑 Conexión a MongoDB cerrada")

def get_database():
    """Devuelve la instancia de la base de datos"""
    return db_instance.db