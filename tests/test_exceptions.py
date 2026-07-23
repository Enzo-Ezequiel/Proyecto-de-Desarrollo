"""Tests de las excepciones de dominio y su mapeo a HTTP."""

import pytest
from http import HTTPStatus

from app.core.exceptions import (
    AppException,
    BusinessLogicException,
    DuplicateResourceException,
    ResourceNotFoundException,
    ValidationException,
)


@pytest.mark.unit
def test_validation_exception_status_code():
    """ValidationException tiene status_code 400."""
    exc = ValidationException("dato inválido")
    assert exc.status_code == HTTPStatus.BAD_REQUEST
    assert exc.error_code == "VALIDATION_ERROR"
    assert exc.message == "dato inválido"


@pytest.mark.unit
def test_resource_not_found_status_code():
    """ResourceNotFoundException tiene status_code 404."""
    exc = ResourceNotFoundException("PDF", "abc-123")
    assert exc.status_code == HTTPStatus.NOT_FOUND
    assert exc.error_code == "RESOURCE_NOT_FOUND"
    assert "PDF" in exc.message
    assert "abc-123" in exc.message


@pytest.mark.unit
def test_duplicate_resource_status_code():
    """DuplicateResourceException tiene status_code 400."""
    exc = DuplicateResourceException("Documento", "checksum xyz")
    assert exc.status_code == HTTPStatus.BAD_REQUEST
    assert exc.error_code == "DUPLICATE_RESOURCE"


@pytest.mark.unit
def test_business_logic_status_code():
    """BusinessLogicException tiene status_code 400."""
    exc = BusinessLogicException("regla violada")
    assert exc.status_code == HTTPStatus.BAD_REQUEST
    assert exc.error_code == "BUSINESS_LOGIC_ERROR"


@pytest.mark.unit
def test_app_exception_base_status_code():
    """AppException base tiene status_code 500."""
    exc = AppException("error general")
    assert exc.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert exc.error_code == "INTERNAL_ERROR"


@pytest.mark.unit
def test_exceptions_son_subclases_de_app_exception():
    """Todas las excepciones específicas son subclases de AppException."""
    assert issubclass(ValidationException, AppException)
    assert issubclass(ResourceNotFoundException, AppException)
    assert issubclass(DuplicateResourceException, AppException)
    assert issubclass(BusinessLogicException, AppException)


@pytest.mark.unit
def test_exception_handler_en_app(client):
    """El exception handler global traduce AppException a la respuesta HTTP correcta."""
    # Forzar una ResourceNotFoundException intentando obtener un ID inexistente
    response = client.get("/api/v1/pdfs/no-existe")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


@pytest.mark.unit
def test_exception_handler_validacion(client):
    """El exception handler traduce ValidationException a 400."""
    archivo = {"file": ("test.txt", b"no pdf", "text/plain")}
    response = client.post("/api/v1/pdfs/", files=archivo)
    assert response.status_code == 400
    assert "PDF válido" in response.json()["detail"]
