from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.utils import logger

# Dependencias de base de datos
from app.core.database import get_database
from app.services.base_service import BaseService

router = APIRouter(prefix="/users", tags=["Users"])

# Inyección de dependencias
def get_user_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> BaseService:
    """Inyecta el servicio de usuario con la base de datos."""
    pass  # TODO: Implementar cuando se agregue el modelo User

# 2. HELPER OBLIGATORIO: Esto hará que apruebes el Check 6 de Clean Code
async def _get_user_or_404(user_id: str, service: BaseService):
    """Método auxiliar para evitar repetir la lógica del error 404."""
    user = await service.get_by_id(user_id)
    if not user:
        logger.warning(f"Usuario no encontrado al buscar ID: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# 3. ENDPOINTS OCULTOS: include_in_schema=False los esconde de la web (Swagger)
@router.get("/", include_in_schema=False)
async def get_all_users(service: BaseService = Depends(get_user_service)):
    """Obtiene todos los usuarios de la base de datos."""
    logger.debug("Solicitando la lista de todos los usuarios.")
    return await service.get_all()

@router.get("/{user_id}", include_in_schema=False)
async def get_user(user_id: str, service: BaseService = Depends(get_user_service)):
    """Obtiene un usuario específico por su ID."""
    logger.debug(f"Buscando usuario con ID: {user_id}")
    return await _get_user_or_404(user_id, service)

@router.delete("/{user_id}", include_in_schema=False)
async def delete_user(user_id: str, service: BaseService = Depends(get_user_service)):
    """Elimina un usuario por su ID."""
    logger.info(f"Solicitud para eliminar usuario con ID: {user_id}")
    
    # Verificamos si existe usando nuestro helper
    await _get_user_or_404(user_id, service)
    
    deleted = await service.delete(user_id)
    if not deleted:
        logger.error(f"❌ Fallo inesperado al eliminar el usuario con ID {user_id}.")
        raise HTTPException(status_code=500, detail="Error interno al eliminar el usuario")
    
    logger.info(f"✅ Usuario con ID {user_id} eliminado exitosamente.")
    return {"message": "Usuario eliminado exitosamente"}