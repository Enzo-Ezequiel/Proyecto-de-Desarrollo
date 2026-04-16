"""
Tests para la capa de Modelos.

Pruebas unitarias para validar la lógica de las entidades.
"""

import pytest
from uuid import uuid4

from app.models import User


class TestUserModel:
    """Suite de tests para el modelo User."""

    def test_user_creation_success(self) -> None:
        """Verifica que un usuario se crea correctamente."""
        user = User(
            email="test@example.com",
            full_name="Test User",
            description="Test description",
        )

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.description == "Test description"
        assert user.is_active is True
        assert user.id is not None

    def test_user_creation_with_short_name(self) -> None:
        """Verifica que se lanza excepción con nombre muy corto."""
        with pytest.raises(ValueError, match="al menos 2 caracteres"):
            User(email="test@example.com", full_name="A")

    def test_user_deactivation(self) -> None:
        """Verifica que un usuario se puede desactivar."""
        user = User(email="test@example.com", full_name="Test User")
        assert user.is_active is True

        user.deactivate()
        assert user.is_active is False

    def test_user_activation(self) -> None:
        """Verifica que un usuario se puede activar."""
        user = User(
            email="test@example.com",
            full_name="Test User",
            is_active=False,
        )
        assert user.is_active is False

        user.activate()
        assert user.is_active is True

    def test_user_profile_update(self) -> None:
        """Verifica que el perfil de un usuario se puede actualizar."""
        user = User(email="test@example.com", full_name="Test User")
        original_updated_at = user.updated_at

        user.update_profile(
            full_name="New Name",
            description="New description",
        )

        assert user.full_name == "New Name"
        assert user.description == "New description"
        assert user.updated_at >= original_updated_at

    def test_user_equality(self) -> None:
        """Verifica que la igualdad se basa en el ID."""
        user_id = uuid4()
        user1 = User(
            id=user_id,
            email="test1@example.com",
            full_name="Test User 1",
        )
        user2 = User(
            id=user_id,
            email="test2@example.com",
            full_name="Test User 2",
        )

        assert user1 == user2

    def test_user_hash(self) -> None:
        """Verifica que los usuarios se pueden usar en sets."""
        user1 = User(email="test1@example.com", full_name="Test User 1")
        user2 = User(email="test2@example.com", full_name="Test User 2")

        user_set = {user1, user2}
        assert len(user_set) == 2
