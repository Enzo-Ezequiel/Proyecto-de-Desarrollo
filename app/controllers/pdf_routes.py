from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.core.database import get_database
from app.core.mongo_repository import MongoRepository
from app.core.utils import logger
from app.models.pdf_document import DocumentoPDF
from app.schemas.pdf_schemas import (
    MensajeResponse,
    PDFDocumentResponse,
    PDFUpdate,
    PDFUploadResponse,
)
from app.services.pdf_service import PdfService

router = APIRouter(prefix=f"{settings.api_prefix}/pdfs", tags=["Documentos PDF"])


def get_pdf_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> PdfService:
    """Inyecta el servicio de PDFs con su repositorio de MongoDB."""
    repository = MongoRepository(db=db, collection_name="pdfs", entity_class=DocumentoPDF)
    return PdfService(repository)


@router.post("/", response_model=PDFUploadResponse, status_code=status.HTTP_201_CREATED)
async def registrar_pdf(
    file: UploadFile = File(...),
    service: PdfService = Depends(get_pdf_service),
):
    """Sube un archivo físico PDF, valida su formato y lo envía al servicio para procesamiento en memoria."""
    logger.info(f"Recibiendo solicitud para registrar PDF: {file.filename}")

    if file.content_type != "application/pdf":
        logger.warning(
            f"Rechazado: El archivo '{file.filename}' no es un PDF válido (Tipo: {file.content_type})."
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un documento PDF válido.",
        )

    documento_guardado = await service.procesar_y_guardar(file)
    logger.info(f"PDF '{file.filename}' procesado y guardado correctamente.")
    return {"mensaje": "✅ PDF procesado y guardado con éxito", "datos": documento_guardado}


@router.get("/", response_model=List[PDFDocumentResponse])
async def listar_pdfs(service: PdfService = Depends(get_pdf_service)):
    """Devuelve una lista con todos los documentos PDF procesados."""
    logger.debug("Solicitando la lista de todos los PDFs.")
    return await service.get_all()


@router.get("/{pdf_id}", response_model=PDFDocumentResponse)
async def obtener_pdf(pdf_id: str, service: PdfService = Depends(get_pdf_service)):
    """Busca y devuelve los detalles de un solo PDF mediante su ID."""
    logger.debug(f"Buscando PDF con ID: {pdf_id}")
    pdf = await service.get_by_id(pdf_id)
    if not pdf:
        logger.warning(f"PDF no encontrado al buscar ID: {pdf_id}")
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado.")
    return pdf


@router.patch("/{pdf_id}", response_model=PDFDocumentResponse)
async def actualizar_pdf(
    pdf_id: str,
    datos: PDFUpdate,
    service: PdfService = Depends(get_pdf_service),
):
    """Actualiza los datos editables de un documento PDF ya persistido."""
    logger.info(f"Solicitud para actualizar PDF con ID: {pdf_id}")
    documento = await service.renombrar(pdf_id, datos.nombre_pdf)
    logger.info(f"PDF con ID {pdf_id} actualizado exitosamente.")
    return documento


@router.delete("/{pdf_id}", response_model=MensajeResponse)
async def borrar_pdf(pdf_id: str, service: PdfService = Depends(get_pdf_service)):
    """Elimina un PDF de la base de datos de forma permanente."""
    logger.info(f"Solicitud para eliminar PDF con ID: {pdf_id}")
    exito = await service.delete(pdf_id)
    if not exito:
        logger.warning(f"Fallo al eliminar: PDF con ID {pdf_id} no encontrado.")
        raise HTTPException(
            status_code=404, detail="Documento PDF no encontrado o ya fue eliminado."
        )

    logger.info(f"PDF con ID {pdf_id} eliminado exitosamente.")
    return {"mensaje": "✅ Documento PDF eliminado con éxito."}
