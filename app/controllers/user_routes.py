from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

# Dependencias de base de datos
from app.core.database import get_database
from app.core.mongo_repository import MongoRepository
from app.services.base_service import BaseService

router = APIRouter(prefix="/users", tags=["Users"])


# Inyección de dependencias
def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> BaseService:
    """Inyecta el servicio de usuario con la base de datos."""
    pass  # TODO: Implementar cuando se agregue el modelo User


# Endpoints
@router.get("/")
async def get_all_users(service: BaseService = Depends(get_user_service)):
    """Obtiene todos los usuarios de la base de datos."""
    return await service.get_all()


@router.get("/{user_id}")
async def get_user(user_id: str, service: BaseService = Depends(get_user_service)):
    """Obtiene un usuario específico por su ID."""
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: str, service: BaseService = Depends(get_user_service)):
    """Elimina un usuario por su ID."""
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}
