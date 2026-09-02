"""Fixtures compartidas para tests."""

import os

# Tests herméticos: la suite debe correr sin .env. Settings (app/core/config.py)
# exige MONGO_DB_NAME y DATABASE_URL sin default y se instancia al importar la app,
# así que las fijamos acá con valores de test ANTES de cualquier import de app.*.
# Ningún test se conecta a Mongo (usan InMemoryRepository vía dependency_overrides):
# la URL apunta a un host inexistente a propósito.
os.environ.setdefault("MONGO_DB_NAME", "test_db")
os.environ.setdefault("DATABASE_URL", "mongodb://nonexistent-test-host:27017")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.controllers.pdf_routes import get_pdf_service  # noqa: E402
from app.core.repository import InMemoryRepository  # noqa: E402
from app.main import app  # noqa: E402
from app.services.pdf_service import PdfService  # noqa: E402
from app.services.pdf_text_extractor import PdfTextExtractor  # noqa: E402

TEXTO_PDF_PRUEBA = "Hola mundo desde un PDF de prueba."


def build_minimal_pdf(texto: str = TEXTO_PDF_PRUEBA) -> bytes:
    """Crea PDF mínimo en memoria con texto extraíble por pypdf (sin librerías extra)."""
    contenido_stream = f"BT /F1 18 Tf 20 150 Td ({texto}) Tj ET".encode("latin-1")

    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length %d >>\nstream\n%s\nendstream"
        % (len(contenido_stream), contenido_stream),
    ]

    buffer = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, cuerpo in enumerate(objetos, start=1):
        offsets.append(len(buffer))
        buffer += f"{i} 0 obj\n".encode("latin-1")
        buffer += cuerpo
        buffer += b"\nendobj\n"

    xref_offset = len(buffer)
    buffer += f"xref\n0 {len(objetos) + 1}\n".encode("latin-1")
    buffer += b"0000000000 65535 f \n"
    for offset in offsets:
        buffer += f"{offset:010d} 00000 n \n".encode("latin-1")

    buffer += (
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF"
    ).encode("latin-1")

    return bytes(buffer)


def subir_pdf(
    client: TestClient,
    contenido: bytes | None = None,
    nombre: str = "documento.pdf",
) -> dict:
    """Sube un PDF y devuelve el documento creado (`datos` de la respuesta).

    Atajo para los tests donde la subida es solo preparación (obtener por id,
    renombrar, borrar). Los tests que verifican la subida en sí —PDF válido,
    duplicado, tamaño máximo— hacen el POST explícito.
    """
    if contenido is None:
        contenido = build_minimal_pdf()
    respuesta = client.post(
        "/api/v1/pdfs/",
        files={"file": (nombre, contenido, "application/pdf")},
    )
    assert respuesta.status_code == 201
    return respuesta.json()["datos"]


@pytest.fixture
def pdf_service_fake() -> PdfService:
    """PdfService con repo en memoria (sin MongoDB real)."""
    return PdfService(InMemoryRepository(), PdfTextExtractor())


@pytest.fixture
def client(pdf_service_fake: PdfService):
    """TestClient con repo Mongo reemplazado por en memoria."""
    app.dependency_overrides[get_pdf_service] = lambda: pdf_service_fake
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_pdf_service, None)


@pytest.fixture
def pdf_valido_bytes() -> bytes:
    return build_minimal_pdf()
