"""Fixtures compartidas para los tests."""

import io

import pytest
from fastapi.datastructures import UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import Headers

from app.core.providers import get_pdf_service
from app.core.repository import InMemoryRepository
from app.main import app
from app.services.pdf_service import PdfService

TEXTO_PDF_PRUEBA = "Hola mundo desde un PDF de prueba."


def make_upload_file(data: bytes, filename: str, content_type: str) -> UploadFile:
    """Crea un UploadFile con content_type correctamente seteado."""
    scope_headers = Headers(
        scope={"type": "http", "headers": [(b"content-type", content_type.encode())]}
    )
    return UploadFile(file=io.BytesIO(data), filename=filename, headers=scope_headers)


def build_minimal_pdf(texto: str = TEXTO_PDF_PRUEBA) -> bytes:
    """
    Construye un PDF mínimo válido con texto extraíble por pypdf.

    Estructura PDF:
    - 1 página con un solo bloque de texto (stream)
    """
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

    return _build_pdf_bytes(objetos)


def build_multipage_pdf(textos: list[str] | None = None) -> bytes:
    """
    Construye un PDF con múltiples páginas, cada una con su propio texto.

    Args:
        textos: Lista de textos por página. Si es None, crea 3 páginas genéricas.
    """
    if textos is None:
        textos = ["Primera pagina", "Segunda pagina", "Tercera pagina"]

    streams = []
    for texto in textos:
        streams.append(f"BT /F1 14 Tf 20 150 Td ({texto}) Tj ET".encode("latin-1"))

    num_paginas = len(textos)
    # Object layout: 1=Catalog, 2=Pages, 3=Font, then pairs of (Page, Content)
    font_obj = 3
    first_page_obj = 4

    objetos = []

    # Object 1: Catalog
    objetos.append(b"<< /Type /Catalog /Pages 2 0 R >>")

    # Object 2: Pages
    kids = " ".join(f"{first_page_obj + i * 2} 0 R" for i in range(num_paginas))
    objetos.append(
        f"<< /Type /Pages /Kids [{kids}] /Count {num_paginas} >>".encode("latin-1")
    )

    # Object 3: Font (shared across all pages)
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    # Objects 4+: Pairs of (Page, Content stream)
    next_obj = first_page_obj
    for i, stream in enumerate(streams):
        content_obj = next_obj + 1
        # Page object — references font at object 3
        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] "
            f"/Resources << /Font << /F1 {font_obj} 0 R >> >> "
            f"/Contents {content_obj} 0 R >>".encode("latin-1")
        )
        # Content stream
        objetos.append(
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"\nendstream"
        )
        next_obj += 2

    return _build_pdf_bytes(objetos)


def build_empty_text_pdf() -> bytes:
    """Construye un PDF válido pero sin texto extraíble (página vacía)."""
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] "
        b"/Resources << /Font << /F1 4 0 R >> >> >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]

    return _build_pdf_bytes(objetos)


def _build_pdf_bytes(objetos: list[bytes]) -> bytes:
    """Motor interno: convierte una lista de objetos PDF en bytes válidos."""
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


@pytest.fixture
def pdf_service_fake() -> PdfService:
    """PdfService respaldado por un repositorio en memoria (sin MongoDB real)."""
    return PdfService(InMemoryRepository())


@pytest.fixture
def client(pdf_service_fake: PdfService):
    """TestClient con el repositorio de Mongo reemplazado por uno en memoria."""
    app.dependency_overrides[get_pdf_service] = lambda: pdf_service_fake
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_pdf_service, None)


@pytest.fixture
def pdf_valido_bytes() -> bytes:
    return build_minimal_pdf()


@pytest.fixture
def pdf_multipage_bytes() -> bytes:
    return build_multipage_pdf()


@pytest.fixture
def pdf_vacio_texto_bytes() -> bytes:
    return build_empty_text_pdf()
