from fastapi.testclient import TestClient
from app.main import app

def test_registrar_archivo_formato_invalido():
    """
    Prueba que el sistema rechace un archivo que no sea PDF (Ej: un .txt)
    y devuelva un Error 400.
    """
    # Usar 'with' hace que FastAPI encienda la app por completo y conecte la BD
    with TestClient(app) as client:
        # Simulamos un archivo de texto plano
        archivo_falso = {"file": ("prueba.txt", b"esto es un texto de prueba", "text/plain")}
        
        response = client.post("/pdfs/", files=archivo_falso)
        
        # Verificamos que el servidor haya bloqueado la solicitud
        assert response.status_code == 400
        assert "El archivo debe ser un documento PDF válido" in response.json()["detail"]

def test_obtener_lista_pdfs():
    """
    Prueba que el endpoint GET /pdfs/ funcione y devuelva una lista (vacía o con datos).
    """
    with TestClient(app) as client:
        response = client.get("/pdfs/")
        
        # Verificamos que la petición sea exitosa y el formato sea correcto
        assert response.status_code == 200
        assert isinstance(response.json(), list)