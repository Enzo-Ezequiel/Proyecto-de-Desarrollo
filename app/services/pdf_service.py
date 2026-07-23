"""Servicio de negocio para documentos PDF."""

import hashlib
import io

import pypdf
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import DuplicateResourceException, ValidationException
from app.core.repository import Repository
from app.models.pdf_document import DocumentoPDF
from app.services.base_service import BaseService


class PdfService(BaseService[DocumentoPDF]):
    """
    Orquesta la validación, extracción de texto y persistencia de documentos PDF.

    Las operaciones CRUD genéricas (get_all, get_by_id, delete) las hereda
    directamente de BaseService; acá solo vive la lógica propia del dominio PDF.
    """

    def __init__(self, repository: Repository[DocumentoPDF]) -> None:
        super().__init__(repository)

    async def procesar_y_guardar(self, file: UploadFile) -> DocumentoPDF:
        """Valida formato, tamaño y duplicados. Extrae texto y persiste el PDF."""
        self._validar_formato(file)
        contenido_bytes = await file.read()

        self._validar_tamano(contenido_bytes)
        self._validar_contenido(contenido_bytes)

        checksum = hashlib.sha256(contenido_bytes).hexdigest()
        await self._validar_no_duplicado(checksum)

        texto_extraido = self._extraer_texto(contenido_bytes)

        nuevo_documento = DocumentoPDF(
            nombre_pdf=file.filename,
            contenido_pdf=texto_extraido,
            checksum=checksum,
        )
        return await self.create(nuevo_documento)

    def _validar_formato(self, file: UploadFile) -> None:
        """Valida que el archivo tenga formato PDF."""
        if file.content_type != "application/pdf":
            raise ValidationException(
                f"El archivo debe ser un documento PDF válido. "
                f"Tipo recibido: {file.content_type}"
            )

    def _validar_tamano(self, contenido_bytes: bytes) -> None:
        limite_mb = settings.pdf_max_size_mb
        if len(contenido_bytes) > (limite_mb * 1024 * 1024):
            raise ValidationException(
                f"El archivo excede el tamaño máximo permitido de {limite_mb}MB."
            )

    def _validar_contenido(self, contenido_bytes: bytes) -> None:
        """Valida que el archivo no esté vacío."""
        if len(contenido_bytes) == 0:
            raise ValidationException("El archivo está vacío.")

    async def _validar_no_duplicado(self, checksum: str) -> None:
        duplicado = await self._repository.find_one({"checksum": checksum})
        if duplicado:
            raise DuplicateResourceException("Documento PDF", f"checksum {checksum}")

    def _extraer_texto(self, contenido_bytes: bytes) -> str:
        try:
            lector_pdf = pypdf.PdfReader(io.BytesIO(contenido_bytes))
        except pypdf.errors.EmptyFileError:
            raise ValidationException("El archivo PDF está vacío o corrupto.")
        except Exception:
            raise ValidationException("No se pudo leer el archivo PDF.")

        texto_extraido = ""
        for pagina in lector_pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_extraido += texto + "\n"
        return texto_extraido.strip()
