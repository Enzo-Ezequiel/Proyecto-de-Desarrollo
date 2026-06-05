from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.pdf_service import procesar_y_guardar_pdf, obtener_todos_los_pdfs, obtener_pdf_por_id, eliminar_pdf

# 1. Importamos nuestro logger
from app.core.utils import logger

router = APIRouter(tags=["Documentos PDF"])

@router.post("/api/v1/pdfs/")
async def registrar_pdf(file: UploadFile = File(...)):
    """Sube un archivo físico PDF, valida su formato y lo envía al servicio para procesamiento en memoria."""
    # Logueamos información útil al iniciar la petición
    logger.info(f"Recibiendo solicitud para registrar PDF: {file.filename}")

    if file.content_type != "application/pdf":
        # 2. Registramos una advertencia si el usuario sube algo que no es PDF
        logger.warning(f"Rechazado: El archivo '{file.filename}' no es un PDF válido (Tipo: {file.content_type}).")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un documento PDF válido."
        )
    
    try:
        documento_guardado = await procesar_y_guardar_pdf(file)
        # 3. Registramos el éxito de la operación
        logger.info(f"✅ PDF '{file.filename}' procesado y guardado correctamente.")
        return {"mensaje": "✅ PDF procesado y guardado con éxito", "datos": documento_guardado}
    except ValueError as e:
        # 4. Registramos como advertencia los errores de validación
        logger.warning(f"Error de validación al procesar '{file.filename}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 5. Registramos como ERROR crítico cualquier fallo inesperado del servidor
        logger.error(f"❌ Error interno al procesar el PDF '{file.filename}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/api/v1/pdfs/")
async def listar_pdfs():
    """Devuelve una lista con todos los documentos PDF procesados."""
    logger.debug("Solicitando la lista de todos los PDFs.")
    return await obtener_todos_los_pdfs()

@router.get("/api/v1/pdfs/{pdf_id}")
async def obtener_pdf(pdf_id: str):
    """Busca y devuelve los detalles de un solo PDF mediante su ID."""
    logger.debug(f"Buscando PDF con ID: {pdf_id}")
    pdf = await obtener_pdf_por_id(pdf_id)
    if not pdf:
        logger.warning(f"PDF no encontrado al buscar ID: {pdf_id}")
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado.")
    return pdf

@router.delete("/api/v1/pdfs/{pdf_id}")
async def borrar_pdf(pdf_id: str):
    """Elimina un PDF de la base de datos de forma permanente."""
    logger.info(f"Solicitud para eliminar PDF con ID: {pdf_id}")
    exito = await eliminar_pdf(pdf_id)
    if not exito:
        logger.warning(f"Fallo al eliminar: PDF con ID {pdf_id} no encontrado.")
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado o ya fue eliminado.")
    
    logger.info(f"✅ PDF con ID {pdf_id} eliminado exitosamente.")
    return {"mensaje": "✅ Documento PDF eliminado con éxito."}