"""
Conexión a MongoDB.

En la arquitectura actual usa un singleton global para compatibilidad
con el lifespan de FastAPI. Para microservicios, cada servicio
instancia su propia DatabaseConnection vía Depends().
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.core.utils import logger


class DatabaseConnection:
    """Encapsula la conexión a MongoDB. Cada microservicio instanciaría la suya."""

    def __init__(self, database_url: str, db_name: str) -> None:
        self._client: AsyncIOMotorClient | None = None
        self._database_url = database_url
        self._db_name = db_name

    @property
    def db(self) -> AsyncIOMotorDatabase | None:
        return self._client[self._db_name] if self._client else None

    async def connect(self) -> None:
        try:
            self._client = AsyncIOMotorClient(self._database_url)
            logger.info("Conectado a MongoDB")
        except Exception as e:
            logger.error(f"Fallo crítico al intentar conectar a MongoDB: {e}")
            raise

    async def disconnect(self) -> None:
        if self._client is not None:
            self._client.close()
            logger.info("Conexión a MongoDB cerrada")


# Singleton global (suficiente para monolito; en microservicios se reemplaza por DI)
_db_connection = DatabaseConnection(settings.database_url, settings.mongo_db_name)


async def connect_to_mongo() -> None:
    """Hook de lifespan: abre la conexión."""
    await _db_connection.connect()


async def close_mongo_connection() -> None:
    """Hook de lifespan: cierra la conexión."""
    await _db_connection.disconnect()


def get_database() -> AsyncIOMotorDatabase:
    """FastAPI Depends(): retorna la instancia de la base de datos.

    Para microservicios, cada servicio redefiniría esta función
    apuntando a su propia DatabaseConnection.
    """
    return _db_connection.db
