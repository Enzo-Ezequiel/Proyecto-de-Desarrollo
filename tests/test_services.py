"""
Tests para la capa de Servicios.

Pruebas unitarias para la lógica de negocio.
"""

import pytest

from app.models import User
from app.services import UserService


class TestUserService:
    """Suite de tests para el servicio UserService."""

    @pytest.fixture
    def service(self) -> UserService:
        """Fixture que proporciona una instancia limpia del servicio."""
        return UserService()

    def test_create_user_success(self, service: UserService) -> None:
        """Verifica la creación exitosa de un usuario."""
        user = service.create_user(
            email="test@example.com",
            full_name="Test User",
            description="Test description",
        )

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert service.count() == 1

    def test_create_duplicate_email(self, service: UserService) -> None:
        """Verifica que no se puede crear usuarios con el mismo email."""
        service.create_user(
            email="test@example.com",
            full_name="User 1",
        )

        with pytest.raises(ValueError, match="ya está registrado"):
            service.create_user(
                email="test@example.com",
                full_name="User 2",
            )

    def test_get_user_by_email(self, service: UserService) -> None:
        """Verifica búsqueda de usuario por email."""
        user = service.create_user(
            email="test@example.com",
            full_name="Test User",
        )

        found_user = service.get_by_email("test@example.com")
        assert found_user is not None
        assert found_user.id == user.id

    def test_email_exists(self, service: UserService) -> None:
        """Verifica si un email existe."""
        service.create_user(
            email="test@example.com",
            full_name="Test User",
        )

        assert service.email_exists("test@example.com") is True
        assert service.email_exists("other@example.com") is False

    def test_get_active_users(self, service: UserService) -> None:
        """Verifica obtención de usuarios activos."""
        user1 = service.create_user(
            email="user1@example.com",
            full_name="User 1",
        )
        user2 = service.create_user(
            email="user2@example.com",
            full_name="User 2",
        )
        service.create_user(
            email="user3@example.com",
            full_name="User 3",
            is_active=False,
        )

        active_users = service.get_active_users()
        assert len(active_users) == 2
        assert user1 in active_users
        assert user2 in active_users

    def test_deactivate_user(self, service: UserService) -> None:
        """Verifica desactivación de usuario."""
        user = service.create_user(
            email="test@example.com",
            full_name="Test User",
        )

        deactivated = service.deactivate_user(user.id)
        assert deactivated is not None
        assert deactivated.is_active is False

    def test_activate_user(self, service: UserService) -> None:
        """Verifica activación de usuario."""
        user = service.create_user(
            email="test@example.com",
            full_name="Test User",
            is_active=False,
        )

        activated = service.activate_user(user.id)
        assert activated is not None
        assert activated.is_active is True

    def test_get_total_active_users(self, service: UserService) -> None:
        """Verifica conteo de usuarios activos."""
        service.create_user(
            email="user1@example.com",
            full_name="User 1",
        )
        service.create_user(
            email="user2@example.com",
            full_name="User 2",
        )
        service.create_user(
            email="user3@example.com",
            full_name="User 3",
            is_active=False,
        )

        assert service.get_total_active_users() == 2
