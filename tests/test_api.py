"""
Tests de integración para los endpoints FastAPI.

Pruebas que verifican todo el flujo: Controlador -> Servicio -> Modelo.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Fixture que proporciona un cliente de prueba para FastAPI."""
    return TestClient(app)


class TestUserEndpoints:
    """Suite de tests para los endpoints de usuarios."""

    def test_health_check(self, client: TestClient) -> None:
        """Verifica que el endpoint de health check funciona."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_root_endpoint(self, client: TestClient) -> None:
        """Verifica que el endpoint raíz funciona."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_create_user(self, client: TestClient) -> None:
        """Verifica creación de usuario vía API."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "description": "Test description",
        }

        response = client.post("/api/v1/users", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["full_name"] == "Test User"
        assert data["is_active"] is True

    def test_list_users(self, client: TestClient) -> None:
        """Verifica listado de usuarios."""
        # Crear algunos usuarios
        for i in range(3):
            client.post(
                "/api/v1/users",
                json={
                    "email": f"user{i}@example.com",
                    "full_name": f"User {i}",
                },
            )

        response = client.get("/api/v1/users")
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert data["total"] >= 3

    def test_get_user_by_id(self, client: TestClient) -> None:
        """Verifica obtención de usuario por ID."""
        # Crear un usuario
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
            },
        )
        user_id = create_response.json()["id"]

        # Obtener el usuario
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == "test@example.com"

    def test_get_nonexistent_user(self, client: TestClient) -> None:
        """Verifica error al obtener usuario inexistente."""
        response = client.get("/api/v1/users/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_update_user(self, client: TestClient) -> None:
        """Verifica actualización de usuario."""
        # Crear un usuario
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "full_name": "Original Name",
            },
        )
        user_id = create_response.json()["id"]

        # Actualizar el usuario
        update_data = {
            "full_name": "Updated Name",
            "description": "Updated description",
        }
        response = client.put(f"/api/v1/users/{user_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"
        assert data["description"] == "Updated description"

    def test_delete_user(self, client: TestClient) -> None:
        """Verifica eliminación de usuario."""
        # Crear un usuario
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
            },
        )
        user_id = create_response.json()["id"]

        # Eliminar el usuario
        response = client.delete(f"/api/v1/users/{user_id}")
        assert response.status_code == 204

        # Verificar que fue eliminado
        response = client.get(f"/api/v1/users/{user_id}")
        assert response.status_code == 404

    def test_deactivate_user(self, client: TestClient) -> None:
        """Verifica desactivación de usuario vía API."""
        # Crear un usuario
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
            },
        )
        user_id = create_response.json()["id"]

        # Desactivar el usuario
        response = client.post(f"/api/v1/users/{user_id}/deactivate")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False

    def test_activate_user(self, client: TestClient) -> None:
        """Verifica activación de usuario vía API."""
        # Crear un usuario inactivo
        create_response = client.post(
            "/api/v1/users",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
            },
        )
        user_id = create_response.json()["id"]

        # Desactivar
        client.post(f"/api/v1/users/{user_id}/deactivate")

        # Activar
        response = client.post(f"/api/v1/users/{user_id}/activate")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is True

    def test_list_active_users_only(self, client: TestClient) -> None:
        """Verifica filtrado de usuarios activos."""
        # Crear usuarios activos
        client.post(
            "/api/v1/users",
            json={"email": "active1@example.com", "full_name": "Active 1"},
        )
        client.post(
            "/api/v1/users",
            json={"email": "active2@example.com", "full_name": "Active 2"},
        )

        # Obtener solo activos
        response = client.get("/api/v1/users?active_only=true")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 2
