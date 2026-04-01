"""
Controlador de Usuarios: Endpoints FastAPI para gestionar usuarios.

Principios aplicados:
- Separation of Concerns: Los controladores solo manejan HTTP.
- Inyección de dependencias: Los servicios se inyectan en los endpoints.
- Documentación automática: Los esquemas Pydantic documentan la API.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.exceptions import AppException
from app.models import User
from app.schemas.user_schemas import (
    ErrorResponse,
    UserCreateRequest,
    UserListResponse,
    UserResponse,
    UserUpdateRequest,
)
from app.services import UserService

# Crear router para usuarios
router = APIRouter(prefix="/users", tags=["users"])


# Dependencia para obtener el servicio de usuarios
def get_user_service() -> UserService:
    """Factory para inyectar el servicio de usuarios."""
    return UserService()


# Funciones auxiliares privadas para manejo de errores


def _get_user_or_404(user_id: UUID, service: UserService) -> User:
    """
    Obtiene un usuario por ID o lanza una excepción 404.

    Implementa el patrón DRY para evitar duplicación de validaciones 404
    en múltiples endpoints.

    Args:
        user_id: El ID del usuario a buscar.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario encontrado.

    Raises:
        HTTPException: Si el usuario no existe (404).
    """
    user = service.get_by_id(str(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    responses={400: {"model": ErrorResponse}},
)
def create_user(
    request: UserCreateRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Crea un nuevo usuario en el sistema.

    Args:
        request: Datos del usuario a crear.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario creado.

    Raises:
        HTTPException: Si el email ya existe o los datos son inválidos.
    """
    try:
        user = service.create_user(
            email=request.email,
            full_name=request.full_name,
            description=request.description,
        )
        return _user_to_response(user)
    except AppException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.get(
    "",
    response_model=UserListResponse,
    summary="Obtener lista de usuarios",
)
def list_users(
    active_only: bool = False,
    service: UserService = Depends(get_user_service),
) -> UserListResponse:
    """
    Obtiene la lista de usuarios del sistema.

    Args:
        active_only: Si es True, solo devuelve usuarios activos.
        service: Servicio de usuarios inyectado.

    Returns:
        Lista de usuarios con el total.
    """
    if active_only:
        users = service.get_active_users()
    else:
        users = service.get_all()

    return UserListResponse(
        users=[_user_to_response(user) for user in users],
        total=len(users),
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    responses={404: {"model": ErrorResponse}},
)
def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Obtiene un usuario específico por su ID.

    Args:
        user_id: El ID del usuario.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario solicitado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    user = _get_user_or_404(user_id, service)
    return _user_to_response(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    responses={404: {"model": ErrorResponse}},
)
def update_user(
    user_id: UUID,
    request: UserUpdateRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Actualiza los datos de un usuario.

    Args:
        user_id: El ID del usuario a actualizar.
        request: Nuevos datos del usuario.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    user = _get_user_or_404(user_id, service)

    try:
        user.update_profile(
            full_name=request.full_name,
            description=request.description,
        )
        updated_user = service.update(user)
        return _user_to_response(updated_user)
    except AppException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    responses={404: {"model": ErrorResponse}},
)
def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> None:
    """
    Elimina un usuario del sistema.

    Args:
        user_id: El ID del usuario a eliminar.
        service: Servicio de usuarios inyectado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    if not service.delete(str(user_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )


@router.post(
    "/{user_id}/deactivate",
    response_model=UserResponse,
    summary="Desactivar usuario",
    responses={404: {"model": ErrorResponse}},
)
def deactivate_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Desactiva un usuario.

    Args:
        user_id: El ID del usuario a desactivar.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario desactivado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    user = service.deactivate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return _user_to_response(user)


@router.post(
    "/{user_id}/activate",
    response_model=UserResponse,
    summary="Activar usuario",
    responses={404: {"model": ErrorResponse}},
)
def activate_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    Activa un usuario.

    Args:
        user_id: El ID del usuario a activar.
        service: Servicio de usuarios inyectado.

    Returns:
        El usuario activado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    user = service.activate_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado",
        )
    return _user_to_response(user)


# Funciones auxiliares privadas


def _user_to_response(user: User) -> UserResponse:
    """
    Convierte un modelo de Usuario a un esquema de respuesta.

    Args:
        user: El usuario a convertir.

    Returns:
        Esquema de respuesta del usuario.
    """
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        description=user.description,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
