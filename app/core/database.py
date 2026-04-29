"""
Conexión a MongoDB.

Proporciona cliente singleton y bases de datos MongoDB.
Principios aplicados:
- Singleton: Una sola conexión para toda la aplicación.
- DRY: Centraliza la configuración de conexión.
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_client() -> AsyncIOMotorClient:
    """
    Obtiene el cliente singleton de MongoDB.

    Returns:
        Cliente de MongoDB.

    Raises:
        RuntimeError: Si no se puede conectar a MongoDB.
    """
    global _client

    if _client is None:
        uri = f"mongodb://{settings.mongodb_host}:{settings.mongodb_port}"
        _client = AsyncIOMotorClient(uri)

    return _client


def get_database() -> AsyncIOMotorDatabase:
    """
    Obtiene la base de datos configurada.

    Returns:
        Base de datos MongoDB.
    """
    global _db

    if _db is None:
        client = get_client()
        _db = client[settings.mongodb_name]

    return _db


def get_collection(name: str):
    """
    Obtiene una colección de la base de datos.

    Args:
        name: Nombre de la colección.

    Returns:
        Colección MongoDB.
    """
    db = get_database()
    return db[name]


async def close_connection() -> None:
    """Cierra la conexión a MongoDB."""
    global _client, _db

    if _client is not None:
        _client.close()
        _client = None
        _db = None
