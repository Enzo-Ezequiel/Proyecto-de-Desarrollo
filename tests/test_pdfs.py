import asyncio
import io

import pytest
from fastapi import UploadFile

from app.core.exceptions import DuplicateResourceException
from app.core.repository import InMemoryRepository
from app.services.pdf_service import PdfService
from tests.conftest import TEXTO_PDF_PRUEBA, build_minimal_pdf


def test_registrar_archivo_formato_invalido(client):
    """Prueba que el sistema rechace un archivo que no sea PDF y devuelva un Error 400."""
    archivo_falso = {
        "file": ("prueba.txt", b"esto es un texto de prueba", "text/plain")
    }

    response = client.post("/api/v1/pdfs/", files=archivo_falso)
    assert response.status_code == 400
    assert (
        "El archivo debe ser un documento PDF válido" in response.json()["detail"]
    )


def test_obtener_lista_pdfs_vacia(client):
    """Prueba que el endpoint GET funcione y devuelva una lista vacía sin PDFs cargados."""
    response = client.get("/api/v1/pdfs/")
    assert response.status_code == 200
    assert response.json() == []


def test_registrar_pdf_valido_extrae_texto(client, pdf_valido_bytes):
    """Un PDF válido se acepta (201), se persiste y el texto extraído coincide con el contenido real."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}

    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 201
    datos = response.json()["datos"]
    assert datos["nombre_pdf"] == "documento.pdf"
    assert TEXTO_PDF_PRUEBA in datos["contenido_pdf"]
    assert len(datos["checksum"]) == 64  # sha256 hexdigest


def test_registrar_pdf_duplicado_es_rechazado(client, pdf_valido_bytes):
    """El mismo PDF (mismo checksum) no puede registrarse dos veces."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}

    primera = client.post("/api/v1/pdfs/", files=archivo)
    assert primera.status_code == 201

    segunda = client.post("/api/v1/pdfs/", files=archivo)
    assert segunda.status_code == 400
    assert "ya existe" in segunda.json()["detail"]


def test_registrar_pdf_excede_tamano_maximo(client):
    """
    Un archivo que excede PDF_MAX_SIZE_MB es rechazado por el FileSizeLimitMiddleware
    (413) antes de llegar al servicio, ya que ambos usan el mismo límite configurado.
    """
    pdf_grande = build_minimal_pdf() + bytes(6 * 1024 * 1024)  # ~6MB > límite (5MB)
    archivo = {"file": ("grande.pdf", pdf_grande, "application/pdf")}

    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 413
    assert "5MB" in response.json()["detail"]


def test_obtener_pdf_por_id_existente(client, pdf_valido_bytes):
    """GET /pdfs/{id} devuelve el documento correcto cuando existe."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]

    response = client.get(f"/api/v1/pdfs/{creado['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == creado["id"]
    assert response.json()["nombre_pdf"] == "documento.pdf"


def test_obtener_pdf_por_id_inexistente(client):
    """GET /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.get("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


def test_actualizar_nombre_pdf_existente(client, pdf_valido_bytes):
    """PATCH /pdfs/{id} renombra el documento y refresca updated_at."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]

    response = client.patch(
        f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": "renombrado.pdf"}
    )

    assert response.status_code == 200
    actualizado = response.json()
    assert actualizado["nombre_pdf"] == "renombrado.pdf"
    assert actualizado["id"] == creado["id"]
    # El contenido y el checksum no se tocan al renombrar
    assert actualizado["checksum"] == creado["checksum"]
    assert actualizado["contenido_pdf"] == creado["contenido_pdf"]

    # El cambio quedó persistido, no es solo la respuesta
    relectura = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert relectura.json()["nombre_pdf"] == "renombrado.pdf"


def test_actualizar_pdf_inexistente(client):
    """PATCH /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.patch(
        "/api/v1/pdfs/id-que-no-existe", json={"nombre_pdf": "otro.pdf"}
    )
    assert response.status_code == 404


def test_actualizar_pdf_con_nombre_vacio_es_rechazado(client, pdf_valido_bytes):
    """PATCH /pdfs/{id} valida el body con Pydantic y rechaza un nombre vacío (422)."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]

    response = client.patch(f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": ""})

    assert response.status_code == 422


def test_borrar_pdf_existente(client, pdf_valido_bytes):
    """DELETE /pdfs/{id} elimina el documento y un GET posterior devuelve 404."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]

    borrado = client.delete(f"/api/v1/pdfs/{creado['id']}")
    assert borrado.status_code == 200

    posterior = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert posterior.status_code == 404


def test_borrar_pdf_inexistente(client):
    """DELETE /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.delete("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


def test_pdf_service_unitario_sin_mongo(pdf_valido_bytes):
    """
    Unit test puro de PdfService (sin HTTP, sin Mongo): usa InMemoryRepository
    para validar extracción de texto y detección de duplicados por checksum.
    """
    service = PdfService(InMemoryRepository())

    async def _ejercitar_servicio():
        subida = UploadFile(file=io.BytesIO(pdf_valido_bytes), filename="a.pdf")
        documento = await service.procesar_y_guardar(subida)
        assert TEXTO_PDF_PRUEBA in documento.contenido_pdf

        subida_duplicada = UploadFile(file=io.BytesIO(pdf_valido_bytes), filename="a.pdf")
        with pytest.raises(DuplicateResourceException):
            await service.procesar_y_guardar(subida_duplicada)

    asyncio.run(_ejercitar_servicio())
