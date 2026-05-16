from fastapi.testclient import TestClient
from app.main import app

def test_registrar_archivo_formato_invalido():
    """Prueba que el sistema rechace un archivo que no sea PDF y devuelva un Error 400."""
    with TestClient(app) as client:
        archivo_falso = {"file": ("prueba.txt", b"esto es un texto de prueba", "text/plain")}
        
        # 👇 Aquí cambiamos a la nueva ruta
        response = client.post("/api/v1/pdfs/", files=archivo_falso)
        assert response.status_code == 400
        assert "El archivo debe ser un documento PDF válido" in response.json()["detail"]

def test_obtener_lista_pdfs():
    """Prueba que el endpoint GET funcione y devuelva una lista."""
    with TestClient(app) as client:
        # 👇 Aquí también cambiamos a la nueva ruta
        response = client.get("/api/v1/pdfs/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)