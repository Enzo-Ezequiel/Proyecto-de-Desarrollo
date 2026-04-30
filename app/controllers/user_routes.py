from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import List

# Importamos la conexión a la base de datos, nuestro nuevo repositorio y el servicio base
from app.core.database import get_database
from app.core.mongo_repository import MongoRepository
from app.services.base_service import BaseService

# TODO: Aquí deberás importar tus modelos y schemas reales que tengas en esas carpetas
# from app.models.user import User  (Entidad de dominio)
# from app.schemas.user import UserCreate, UserResponse (Validaciones Pydantic)

router = APIRouter(prefix="/users", tags=["Users"])

# =====================================================================
# 1. INYECCIÓN DE DEPENDENCIAS (Conectando las capas)
# =====================================================================
def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> BaseService:
    """
    FastAPI inyectará la base de datos aquí. Nosotros instanciamos el 
    MongoRepository y se lo pasamos al servicio genérico.
    """
    # IMPORTANTE: Descomenta esto y reemplaza 'User' por tu clase modelo real
    # repository = MongoRepository(db, "users", User)
    # return BaseService(repository)
    pass # Quita este pass cuando descomentes las líneas de arriba


# =====================================================================
# 2. ENDPOINTS ASÍNCRONOS (Capa 3: Solo HTTP)
# =====================================================================
@router.get("/")
async def get_all_users(service: BaseService = Depends(get_user_service)):
    """Obtiene todos los usuarios de la base de datos."""
    # Como el servicio ahora es asíncrono, usamos 'await'
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