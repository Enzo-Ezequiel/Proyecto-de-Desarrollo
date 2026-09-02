"""Lógica de negocio para PDFs: validación, deduplicado y persistencia."""

import hashlib

from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import (
    DuplicateResourceException,
    ResourceNotFoundException,
    ValidationException,
)
from app.core.repository import Repository
from app.models.pdf_document import DocumentoPDF
from app.services.base_service import BaseService
from app.services.pdf_text_extractor import PdfTextExtractor


class PdfService(BaseService[DocumentoPDF]):
    """Servicio específico de PDFs. Lo común (CRUD) viene de BaseService."""

    def __init__(
        self,
        repository: Repository[DocumentoPDF],
        text_extractor: PdfTextExtractor,
    ) -> None:
        super().__init__(repository)
        self._text_extractor = text_extractor

    async def procesar_y_guardar(self, file: UploadFile) -> DocumentoPDF:
        """Valida archivo, verifica duplicados y guarda."""
        self._validar_formato(file)
        contenido_bytes = await file.read()

        self._validar_tamano(contenido_bytes)
        checksum = hashlib.sha256(contenido_bytes).hexdigest()
        await self._validar_no_duplicado(checksum)

        texto_extraido = self._text_extractor.extraer_texto(contenido_bytes)

        nuevo_documento = DocumentoPDF(
            nombre_pdf=file.filename,
            contenido_pdf=texto_extraido,
            checksum=checksum,
        )
        return await self.create(nuevo_documento)

    async def renombrar(self, pdf_id: str, nuevo_nombre: str) -> DocumentoPDF:
        """Renombra PDF y actualiza timestamp."""
        documento = await self.get_by_id(pdf_id)
        if documento is None:
            raise ResourceNotFoundException("Documento PDF", pdf_id)

        documento.nombre_pdf = nuevo_nombre
        documento.update_timestamp()
        return await self.update(documento)

    def _validar_formato(self, file: UploadFile) -> None:
        """Rechaza archivos cuyo content-type no sea application/pdf (-> 400).

        Qué formatos acepta el negocio es una regla de dominio, no de la capa HTTP.
        """
        if file.content_type != "application/pdf":
            raise ValidationException("El archivo debe ser un PDF válido.")

    def _validar_tamano(self, contenido_bytes: bytes) -> None:
        """Valida el tamaño real del PDF ya leído; lanza ValidationException (-> 400).

        Segunda capa de la defensa en profundidad sobre el límite de tamaño.
        FileSizeLimitMiddleware ya rechaza con 413 las peticiones cuyo header
        Content-Length supera el límite, pero ese header puede faltar o ser falso;
        acá se mide el contenido efectivo. El 400 (vs. el 413 del middleware) marca
        que el cuerpo se recibió entero y es la regla de negocio la que lo rechaza.
        """
        limite_mb = settings.pdf_max_size_mb
        if len(contenido_bytes) > (limite_mb * 1024 * 1024):
            raise ValidationException(
                f"El archivo excede el tamaño máximo de {limite_mb}MB."
            )

    async def _validar_no_duplicado(self, checksum: str) -> None:
        duplicado = await self._repository.find_one({"checksum": checksum})
        if duplicado:
            raise DuplicateResourceException("Documento PDF", f"checksum {checksum}")
