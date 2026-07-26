from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PDFUpdate(BaseModel):
    """Campos editables de un documento PDF ya persistido."""

    nombre_pdf: str = Field(min_length=1, max_length=255)


class PDFDocumentResponse(BaseModel):
    """Representación pública de un documento PDF persistido."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_pdf: str
    contenido_pdf: str
    checksum: str
    created_at: datetime
    updated_at: datetime


class PDFUploadResponse(BaseModel):
    """Respuesta del endpoint de registro de un PDF."""

    mensaje: str
    datos: PDFDocumentResponse


class MensajeResponse(BaseModel):
    """Respuesta simple de confirmación (ej. borrado exitoso)."""

    mensaje: str
