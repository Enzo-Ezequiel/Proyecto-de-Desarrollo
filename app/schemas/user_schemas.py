"""
Esquemas Pydantic para validación y serialización de datos de API.

Principios aplicados:
- Separación de responsabilidades: Los esquemas están separados de los modelos de dominio.
- Single Responsibility: Cada esquema representa un solo contrato de API.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    """
    Esquema para la solicitud de creación de usuario.

    Valida los datos enviados por el cliente al crear un usuario.
    """

    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción o biografía del usuario",
    )


class UserUpdateRequest(BaseModel):
    """
    Esquema para la solicitud de actualización de usuario.

    Solo permite actualizar ciertos campos.
    """

    full_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción o biografía del usuario",
    )


class UserResponse(BaseModel):
    """
    Esquema de respuesta para un usuario.

    Incluye todos los campos públicos del usuario.
    """

    id: UUID
    email: str
    full_name: str
    is_active: bool
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "user@example.com",
                "full_name": "Juan Pérez",
                "is_active": True,
                "description": "Desarrollador Python",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }


class UserListResponse(BaseModel):
    """Esquema para una lista de usuarios."""

    users: list[UserResponse]
    total: int

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "users": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "email": "user@example.com",
                        "full_name": "Juan Pérez",
                        "is_active": True,
                        "description": "Desarrollador Python",
                        "created_at": "2024-01-15T10:30:00",
                        "updated_at": "2024-01-15T10:30:00",
                    }
                ],
                "total": 1,
            }
        }


class ErrorResponse(BaseModel):
    """Esquema genérico para respuestas de error."""

    detail: str
    error_code: Optional[str] = None
