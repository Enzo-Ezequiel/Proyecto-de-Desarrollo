import hashlib

import pytest

from app.core.exceptions import (
    DuplicateResourceException,
    ValidationException,
)
from app.core.repository import InMemoryRepository
from app.services.pdf_service import PdfService
from tests.conftest import (
    TEXTO_PDF_PRUEBA,
    build_empty_text_pdf,
    build_minimal_pdf,
    build_multipage_pdf,
    make_upload_file,
)


# ─── Tests de Integración (Controller + Service) ────────────────────────────


@pytest.mark.integration
def test_registrar_archivo_formato_invalido(client):
    """El sistema rechaza un archivo que no sea PDF con Error 400."""
    archivo_falso = {
        "file": ("prueba.txt", b"esto es un texto de prueba", "text/plain")
    }
    response = client.post("/api/v1/pdfs/", files=archivo_falso)
    assert response.status_code == 400
    assert "El archivo debe ser un documento PDF válido" in response.json()["detail"]


@pytest.mark.integration
def test_registrar_archivo_formato_imagen(client):
    """El sistema rechaza un archivo .jpg con Error 400."""
    archivo = {"file": ("foto.jpg", b"\xff\xd8\xff\xe0 fake jpeg", "image/jpeg")}
    response = client.post("/api/v1/pdfs/", files=archivo)
    assert response.status_code == 400


@pytest.mark.integration
def test_obtener_lista_pdfs_vacia(client):
    """GET /pdfs/ devuelve lista vacía cuando no hay PDFs."""
    response = client.get("/api/v1/pdfs/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.integration
def test_registrar_pdf_valido_extrae_texto(client, pdf_valido_bytes):
    """Un PDF válido se acepta (201), se persiste y el texto extraído coincide."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    response = client.post("/api/v1/pdfs/", files=archivo)

    assert response.status_code == 201
    datos = response.json()["datos"]
    assert datos["nombre_pdf"] == "documento.pdf"
    assert TEXTO_PDF_PRUEBA in datos["contenido_pdf"]
    assert len(datos["checksum"]) == 64


@pytest.mark.integration
def test_registrar_pdf_duplicado_es_rechazado(client, pdf_valido_bytes):
    """El mismo PDF (mismo checksum) no puede registrarse dos veces."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    primera = client.post("/api/v1/pdfs/", files=archivo)
    assert primera.status_code == 201

    segunda = client.post("/api/v1/pdfs/", files=archivo)
    assert segunda.status_code == 400
    assert "ya existe" in segunda.json()["detail"]


@pytest.mark.integration
def test_registrar_pdf_excede_tamano_maximo(client):
    """Un archivo que excede PDF_MAX_SIZE_MB es rechazado (413)."""
    pdf_grande = build_minimal_pdf() + bytes(6 * 1024 * 1024)
    archivo = {"file": ("grande.pdf", pdf_grande, "application/pdf")}
    response = client.post("/api/v1/pdfs/", files=archivo)
    assert response.status_code == 413
    assert "5MB" in response.json()["detail"]


@pytest.mark.integration
def test_registrar_archivo_0_bytes(client):
    """Un archivo de 0 bytes es rechazado con Error 400."""
    archivo = {"file": ("vacio.pdf", b"", "application/pdf")}
    response = client.post("/api/v1/pdfs/", files=archivo)
    assert response.status_code == 400
    assert "vacío" in response.json()["detail"]


@pytest.mark.integration
def test_obtener_pdf_por_id_existente(client, pdf_valido_bytes):
    """GET /pdfs/{id} devuelve el documento correcto cuando existe."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]
    response = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == creado["id"]
    assert response.json()["nombre_pdf"] == "documento.pdf"


@pytest.mark.integration
def test_obtener_pdf_por_id_inexistente(client):
    """GET /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.get("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


@pytest.mark.integration
def test_borrar_pdf_existente(client, pdf_valido_bytes):
    """DELETE /pdfs/{id} elimina el documento y un GET posterior devuelve 404."""
    archivo = {"file": ("documento.pdf", pdf_valido_bytes, "application/pdf")}
    creado = client.post("/api/v1/pdfs/", files=archivo).json()["datos"]
    borrado = client.delete(f"/api/v1/pdfs/{creado['id']}")
    assert borrado.status_code == 200
    posterior = client.get(f"/api/v1/pdfs/{creado['id']}")
    assert posterior.status_code == 404


@pytest.mark.integration
def test_borrar_pdf_inexistente(client):
    """DELETE /pdfs/{id} devuelve 404 cuando el id no existe."""
    response = client.delete("/api/v1/pdfs/id-que-no-existe")
    assert response.status_code == 404


@pytest.mark.integration
def test_nombre_archivo_espacio(client, pdf_valido_bytes):
    """Un PDF con espacio en el nombre se acepta correctamente."""
    archivo = {"file": ("mi documento.pdf", pdf_valido_bytes, "application/pdf")}
    response = client.post("/api/v1/pdfs/", files=archivo)
    assert response.status_code == 201
    assert response.json()["datos"]["nombre_pdf"] == "mi documento.pdf"


# ─── Tests Unitarios (Service puro, sin HTTP) ────────────────────────────────


@pytest.mark.unit
def test_pdf_service_extrae_texto(pdf_valido_bytes):
    """El servicio extrae correctamente el texto de un PDF válido."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_valido_bytes, "test.pdf", "application/pdf")
        documento = await service.procesar_y_guardar(subida)
        assert TEXTO_PDF_PRUEBA in documento.contenido_pdf

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_pdf_service_duplicado_lanza_excepcion(pdf_valido_bytes):
    """El servicio lanza DuplicateResourceException al intentar registrar duplicado."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida1 = make_upload_file(pdf_valido_bytes, "a.pdf", "application/pdf")
        await service.procesar_y_guardar(subida1)
        subida2 = make_upload_file(pdf_valido_bytes, "a.pdf", "application/pdf")
        with pytest.raises(DuplicateResourceException):
            await service.procesar_y_guardar(subida2)

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_checksum_es_sha256_correcto(pdf_valido_bytes):
    """El checksum generado es el SHA-256 exacto del contenido del archivo."""
    service = PdfService(InMemoryRepository())
    esperado = hashlib.sha256(pdf_valido_bytes).hexdigest()

    async def _ejercitar():
        subida = make_upload_file(pdf_valido_bytes, "test.pdf", "application/pdf")
        documento = await service.procesar_y_guardar(subida)
        assert documento.checksum == esperado

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_formato_no_pdf_lanza_excepcion():
    """El servicio lanza ValidationException si el content_type no es PDF."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        archivo_falso = make_upload_file(b"no es un pdf", "fake.pdf", "text/plain")
        with pytest.raises(ValidationException, match="PDF válido"):
            await service.procesar_y_guardar(archivo_falso)

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_extract_texto_multi_pagina(pdf_multipage_bytes):
    """El servicio extrae texto de todas las páginas de un PDF multi-página."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_multipage_bytes, "multi.pdf", "application/pdf")
        documento = await service.procesar_y_guardar(subida)
        assert "Primera pagina" in documento.contenido_pdf
        assert "Segunda pagina" in documento.contenido_pdf
        assert "Tercera pagina" in documento.contenido_pdf

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_extract_texto_pagina_vacia(pdf_vacio_texto_bytes):
    """Un PDF sin texto extraíble devuelve contenido_pdf vacío o con espacios."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_vacio_texto_bytes, "vacio.pdf", "application/pdf")
        documento = await service.procesar_y_guardar(subida)
        assert documento.contenido_pdf.strip() == ""

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_pdf_service_crea_entidad_con_campos_correctos(pdf_valido_bytes):
    """La entidad creada tiene todos los campos poblados correctamente."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_valido_bytes, "doc.pdf", "application/pdf")
        documento = await service.procesar_y_guardar(subida)
        assert documento.nombre_pdf == "doc.pdf"
        assert isinstance(documento.checksum, str)
        assert len(documento.checksum) == 64
        assert documento.id is not None
        assert documento.created_at is not None
        assert documento.updated_at is not None

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_pdf_service_get_by_id(pdf_valido_bytes):
    """Service.get_by_id retorna el documento correcto."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_valido_bytes, "doc.pdf", "application/pdf")
        creado = await service.procesar_y_guardar(subida)
        encontrado = await service.get_by_id(creado.id)
        assert encontrado is not None
        assert encontrado.id == creado.id

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_pdf_service_get_all(pdf_valido_bytes):
    """Service.get_all retorna todos los documentos."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida1 = make_upload_file(pdf_valido_bytes, "a.pdf", "application/pdf")
        await service.procesar_y_guardar(subida1)
        contenido_diferente = build_minimal_pdf("Otro texto distinto")
        subida2 = make_upload_file(contenido_diferente, "b.pdf", "application/pdf")
        await service.procesar_y_guardar(subida2)
        todos = await service.get_all()
        assert len(todos) == 2

    import asyncio

    asyncio.run(_ejercitar())


@pytest.mark.unit
def test_pdf_service_delete(pdf_valido_bytes):
    """Service.delete elimina un documento existente."""
    service = PdfService(InMemoryRepository())

    async def _ejercitar():
        subida = make_upload_file(pdf_valido_bytes, "doc.pdf", "application/pdf")
        creado = await service.procesar_y_guardar(subida)
        resultado = await service.delete(creado.id)
        assert resultado is True
        encontrado = await service.get_by_id(creado.id)
        assert encontrado is None

    import asyncio

    asyncio.run(_ejercitar())
