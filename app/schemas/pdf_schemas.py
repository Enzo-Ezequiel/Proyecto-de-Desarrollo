from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
