from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PDFUpdate(BaseModel):
    """Campos editables de un PDF guardado (solo el nombre)."""

    nombre_pdf: str = Field(min_length=1, max_length=255)


class PDFDocumentResponse(BaseModel):
    """Cómo se ve un PDF guardado en la API."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    nombre_pdf: str
    contenido_pdf: str
    checksum: str
    created_at: datetime
    updated_at: datetime


class PDFUploadResponse(BaseModel):
    """Respuesta al subir un PDF: mensaje + datos del documento."""

    mensaje: str
    datos: PDFDocumentResponse


class MensajeResponse(BaseModel):
    """Respuesta simple con solo mensaje (ej. borrado OK)."""

    mensaje: str
