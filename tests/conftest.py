"""
Configuración de pytest para tests.

Define fixtures compartidas y configuración global para los tests.
"""

import pytest

from app.models import User
from app.services import UserService
from app.services.user_service import reset_shared_repository


def pytest_configure(config):
    """Configuración inicial de pytest."""
    config.addinivalue_line(
        "markers",
        "unit: Marca tests unitarios",
    )
    config.addinivalue_line(
        "markers",
        "integration: Marca tests de integración",
    )


@pytest.fixture(autouse=True)
def reset_repository():
    """Reinicia el repositorio antes de cada test."""
    reset_shared_repository()
    yield
    reset_shared_repository()


# ============================================================================
# Test Data Constants - Source of Truth para datos de test
# ============================================================================

TEST_VALID_EMAIL = "test@example.com"
TEST_VALID_NAME = "Test User"
TEST_VALID_DESCRIPTION = "Test description"

USERS_API_ENDPOINT = "/api/v1/users"


# ============================================================================
# Fixtures for Services
# ============================================================================


@pytest.fixture
def user_service() -> UserService:
    """Proporciona una instancia fresca de UserService para cada test."""
    return UserService()


# ============================================================================
# Fixtures for Test Data
# ============================================================================


@pytest.fixture
def test_user_data() -> dict:
    """Proporciona datos válidos para crear un usuario de test."""
    return {
        "email": TEST_VALID_EMAIL,
        "full_name": TEST_VALID_NAME,
        "description": TEST_VALID_DESCRIPTION,
    }


@pytest.fixture
def test_user(user_service: UserService) -> User:
    """Proporciona un usuario de test ya creado."""
    return user_service.create_user(
        email=TEST_VALID_EMAIL,
        full_name=TEST_VALID_NAME,
        description=TEST_VALID_DESCRIPTION,
    )


# ============================================================================
# Helper Functions for Test Factories
# ============================================================================


def create_test_user(
    service: UserService,
    email: str = TEST_VALID_EMAIL,
    full_name: str = TEST_VALID_NAME,
    description: str = TEST_VALID_DESCRIPTION,
) -> User:
    """
    Factory function para crear usuarios de test.

    Esta función centraliza la lógica de creación de usuarios para tests,
    siguiendo el patrón DRY.

    Args:
        service: Servicio UserService a usar.
        email: Email del usuario (por defecto TEST_VALID_EMAIL).
        full_name: Nombre del usuario (por defecto TEST_VALID_NAME).
        description: Descripción del usuario (por defecto TEST_VALID_DESCRIPTION).

    Returns:
        Usuario creado.
    """
    return service.create_user(
        email=email,
        full_name=full_name,
        description=description,
    )


def create_multiple_test_users(service: UserService, count: int = 3) -> list[User]:
    """
    Factory function para crear múltiples usuarios de test.

    Args:
        service: Servicio UserService a usar.
        count: Número de usuarios a crear (por defecto 3).

    Returns:
        Lista de usuarios creados.
    """
    users = []
    for i in range(count):
        user = create_test_user(
            service,
            email=f"user{i}@example.com",
            full_name=f"User {i}",
        )
        users.append(user)
    return users
