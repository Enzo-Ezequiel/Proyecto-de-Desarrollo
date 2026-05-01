from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.pdf_service import procesar_y_guardar_pdf, obtener_todos_los_pdfs, obtener_pdf_por_id, eliminar_pdf

router = APIRouter(tags=["Documentos PDF"])

@router.post("/pdfs/")
async def registrar_pdf(file: UploadFile = File(...)):
    """
    Sube un archivo físico PDF, valida su formato y lo envía al servicio para procesamiento en memoria.
    """
    # Validación de Formato: Nos aseguramos de que sea un PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo debe ser un documento PDF válido."
        )
    
    try:
        # Pasamos el archivo directamente al servicio (Capa 2)
        documento_guardado = await procesar_y_guardar_pdf(file)
        return {
            "mensaje": "✅ PDF procesado y guardado con éxito", 
            "datos": documento_guardado
        }
    except ValueError as e:
        # Errores de negocio (tamaño excedido o duplicados)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/pdfs/")
async def listar_pdfs():
    """Devuelve una lista con todos los documentos PDF procesados."""
    return await obtener_todos_los_pdfs()

@router.get("/pdfs/{pdf_id}")
async def obtener_pdf(pdf_id: str):
    """Busca y devuelve los detalles de un solo PDF mediante su ID."""
    pdf = await obtener_pdf_por_id(pdf_id)
    if not pdf:
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado.")
    return pdf

@router.delete("/pdfs/{pdf_id}")
async def borrar_pdf(pdf_id: str):
    """Elimina un PDF de la base de datos de forma permanente."""
    exito = await eliminar_pdf(pdf_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Documento PDF no encontrado o ya fue eliminado.")
    return {"mensaje": "✅ Documento PDF eliminado con éxito."}