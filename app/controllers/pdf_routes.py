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
from app.services.pdf_text_extractor import PdfTextExtractor

router = APIRouter(prefix=f"{settings.api_prefix}/pdfs", tags=["Documentos PDF"])


def get_pdf_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> PdfService:
    """Inyecta servicio PDF con repo Mongo y extractor de texto."""
    repository = MongoRepository(
        db=db, collection_name="pdfs", entity_class=DocumentoPDF
    )
    return PdfService(repository, PdfTextExtractor())


@router.post("/", response_model=PDFUploadResponse, status_code=status.HTTP_201_CREATED)
async def registrar_pdf(
    file: UploadFile = File(...),
    service: PdfService = Depends(get_pdf_service),
):
    """Sube PDF, lo valida y lo manda a procesar."""
    logger.info(f"Recibiendo PDF: {file.filename}")

    if file.content_type != "application/pdf":
        logger.warning(
            f"Rechazado: '{file.filename}' no es PDF (tipo: {file.content_type})"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un PDF válido.",
        )

    documento_guardado = await service.procesar_y_guardar(file)
    logger.info(f"PDF '{file.filename}' procesado y guardado OK")
    return {
        "mensaje": "✅ PDF procesado y guardado con éxito",
        "datos": documento_guardado,
    }


@router.get("/", response_model=list[PDFDocumentResponse])
async def listar_pdfs(service: PdfService = Depends(get_pdf_service)):
    """Lista todos los PDFs procesados."""
    logger.debug("Pidiendo lista de PDFs")
    return await service.get_all()


@router.get("/{pdf_id}", response_model=PDFDocumentResponse)
async def obtener_pdf(pdf_id: str, service: PdfService = Depends(get_pdf_service)):
    """Busca un PDF por ID."""
    logger.debug(f"Buscando PDF id: {pdf_id}")
    pdf = await service.get_by_id(pdf_id)
    if not pdf:
        logger.warning(f"PDF no encontrado: {pdf_id}")
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado.")
    return pdf


@router.patch("/{pdf_id}", response_model=PDFDocumentResponse)
async def actualizar_pdf(
    pdf_id: str,
    datos: PDFUpdate,
    service: PdfService = Depends(get_pdf_service),
):
    """Renombra un PDF y actualiza fecha."""
    logger.info(f"Actualizando PDF id: {pdf_id}")
    documento = await service.renombrar(pdf_id, datos.nombre_pdf)
    logger.info(f"PDF {pdf_id} actualizado OK")
    return documento


@router.delete("/{pdf_id}", response_model=MensajeResponse)
async def borrar_pdf(pdf_id: str, service: PdfService = Depends(get_pdf_service)):
    """Borra un PDF."""
    logger.info(f"Eliminando PDF id: {pdf_id}")
    exito = await service.delete(pdf_id)
    if not exito:
        logger.warning(f"Fallo al borrar: PDF {pdf_id} no existe")
        raise HTTPException(
            status_code=404, detail="Documento PDF no encontrado o ya fue eliminado."
        )

    logger.info(f"PDF {pdf_id} eliminado OK")
    return {"mensaje": "✅ Documento PDF eliminado con éxito."}
