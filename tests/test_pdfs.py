import io

import pytest
from fastapi import UploadFile

from app.core.exceptions import DuplicateResourceException
from app.core.repository import InMemoryRepository
from app.services.pdf_service import PdfService
from tests.conftest import TEXTO_PDF_PRUEBA, build_minimal_pdf, subir_pdf


@pytest.mark.integration
def test_registrar_archivo_formato_invalido(client):
    """Rechaza archivo no-PDF (400)."""
    archivo_falso = {
        "file": ("prueba.txt", b"esto es un texto de prueba", "text/plain")
    }

    response = client.post("/api/v1/pdfs/", files=archivo_falso)
    assert response.status_code == 400
    assert "El archivo debe ser un PDF válido" in response.json()["detail"]


@pytest.mark.integration
def test_registrar_archivo_con_extension_pdf_pero_content_type_incorrecto(client):
    """Extensión .pdf NO bypasea check de content-type: si MIME no es application/pdf, 400."""
    archivo = {"file": ("truco.pdf", b"contenido falso", "application/octet-stream")}

    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 400
    assert "El archivo debe ser un PDF válido" in response.json()["detail"]


@pytest.mark.integration
def test_obtener_lista_pdfs_vacia(client):
    """GET devuelve lista vacía sin PDFs cargados."""
    response = client.get("/api/v1/pdfs/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
def test_obtener_lista_devuelve_exactamente_los_registrados(client):
    """Tras subir 2 PDFs, GET / lista los 2 nombres en orden de inserción."""
    pdf_a = build_minimal_pdf("Texto del primer documento.")
    pdf_b = build_minimal_pdf("Texto del segundo documento.")

    client.post("/api/v1/pdfs/", files={"file": ("a.pdf", pdf_a, "application/pdf")})
    client.post("/api/v1/pdfs/", files={"file": ("b.pdf", pdf_b, "application/pdf")})

    response = client.get("/api/v1/pdfs/")

    assert response.status_code == 200
    lista = response.json()
    assert len(lista) == 2
    nombres = [item["nombre_pdf"] for item in lista]
    assert nombres == ["a.pdf", "b.pdf"]
    assert lista[0]["checksum"] != lista[1]["checksum"]


@pytest.mark.integration
def test_registrar_pdf_valido_extrae_texto(client, pdf_valido_bytes):
    """PDF válido se acepta (201), persiste y texto extraído coincide."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}

    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 201
    datos = response.json()["datos"]
    assert datos["nombre_pdf"] == "documento.pdf"
    assert TEXTO_PDF_PRUEBA in datos["contenido_pdf"]
    assert len(datos["checksum"]) == 64  # sha256 hex


@pytest.mark.integration
def test_registrar_pdf_duplicado_es_rechazado(client, pdf_valido_bytes):
    """Mismo PDF (mismo checksum) no puede registrarse dos veces."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}

    primera = client.post("/api/v1/pdfs/", files=archivo)
    assert primera.status_code == 201

    segunda = client.post("/api/v1/pdfs/", files=archivo)
    assert segunda.status_code == 400
    assert "ya existe" in segunda.json()["detail"]


@pytest.mark.integration
def test_registrar_pdf_excede_tamano_maximo(client):
    """Archivo > PDF_MAX_SIZE_MB rechazado por middleware (413) antes de llegar al servicio."""
    pdf_grande = build_minimal_pdf() + bytes(6 * 1024 * 1024)  # ~6MB > límite (5MB)
    archivo = {"file": ("grande.pdf", pdf_grande, "application/pdf")}

    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 413
    assert "5MB" in response.json()["detail"]


@pytest.mark.integration
def test_obtener_pdf_por_id_existente(client):
    """GET /pdfs/{id} devuelve documento correcto cuando existe."""
    creado = subir_pdf(client)

    response = client.get(f"/api/v1/pdfs/{creado['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == creado["id"]
    assert response.json()["nombre_pdf"] == "documento.pdf"


@pytest.mark.integration
def test_obtener_pdf_por_id_inexistente(client):
    """GET /pdfs/{id} devuelve 404 cuando id no existe."""
    response = client.get("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


@pytest.mark.integration
def test_actualizar_nombre_pdf_existente(client):
    """PATCH /pdfs/{id} renombra documento y refresca updated_at."""
    creado = subir_pdf(client)

    response = client.patch(
        f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": "renombrado.pdf"}
    )

    assert response.status_code == 200
    actualizado = response.json()
    assert actualizado["nombre_pdf"] == "renombrado.pdf"
    assert actualizado["id"] == creado["id"]
    # Contenido y checksum no cambian al renombrar
    assert actualizado["checksum"] == creado["checksum"]
    assert actualizado["contenido_pdf"] == creado["contenido_pdf"]

    # Cambio persistido
    relectura = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert relectura.json()["nombre_pdf"] == "renombrado.pdf"


@pytest.mark.integration
def test_actualizar_pdf_inexistente(client):
    """PATCH /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.patch(
        "/api/v1/pdfs/id-que-no-existe", json={"nombre_pdf": "otro.pdf"}
    )
    assert response.status_code == 404


@pytest.mark.integration
def test_actualizar_pdf_con_nombre_vacio_es_rechazado(client):
    """PATCH valida body con Pydantic y rechaza nombre vacío (422)."""
    creado = subir_pdf(client)

    response = client.patch(f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": ""})

    assert response.status_code == 422


@pytest.mark.integration
def test_actualizar_pdf_con_nombre_de_255_caracteres_es_aceptado(client):
    """Nombre de exactamente 255 caracteres respeta max_length de PDFUpdate (200)."""
    creado = subir_pdf(client)

    response = client.patch(
        f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": "a" * 255}
    )

    assert response.status_code == 200
    assert response.json()["nombre_pdf"] == "a" * 255


@pytest.mark.integration
def test_actualizar_pdf_con_nombre_de_256_caracteres_es_rechazado(client):
    """Nombre de 256 caracteres excede max_length=255 de PDFUpdate (422)."""
    creado = subir_pdf(client)

    response = client.patch(
        f"/api/v1/pdfs/{creado['id']}", json={"nombre_pdf": "a" * 256}
    )

    assert response.status_code == 422


@pytest.mark.integration
def test_borrar_pdf_existente(client):
    """DELETE /pdfs/{id} elimina y GET posterior devuelve 404."""
    creado = subir_pdf(client)

    borrado = client.delete(f"/api/v1/pdfs/{creado['id']}")
    assert borrado.status_code == 200

    posterior = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert posterior.status_code == 404


@pytest.mark.integration
def test_borrar_pdf_inexistente(client):
    """DELETE /pdfs/{id} devuelve 404 cuando id no existe."""
    response = client.delete("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pdf_service_unitario_sin_mongo(pdf_valido_bytes):
    """Test unitario puro de PdfService (sin HTTP, sin Mongo): InMemoryRepo valida extracción y duplicados."""
    service = PdfService(InMemoryRepository())

    subida = UploadFile(file=io.BytesIO(pdf_valido_bytes), filename="a.pdf")
    documento = await service.procesar_y_guardar(subida)
    assert TEXTO_PDF_PRUEBA in documento.contenido_pdf

    subida_duplicada = UploadFile(file=io.BytesIO(pdf_valido_bytes), filename="a.pdf")
    with pytest.raises(DuplicateResourceException):
        await service.procesar_y_guardar(subida_duplicada)
