from fastapi import APIRouter
from app.schemas.pdf_schemas import PDFCreate
from app.services.pdf_service import guardar_pdf  # Importamos nuestro nuevo servicio

router = APIRouter(tags=["Documentos PDF"])

@router.post("/pdfs/")
async def registrar_pdf(pdf: PDFCreate):
    """
    Recibe la información de un PDF validada por Pydantic 
    y delega su guardado a la Capa de Servicios.
    """
    # Pasamos los datos al servicio para que haga el trabajo sucio con MongoDB
    documento_guardado = await guardar_pdf(pdf)
    
    return {
        "mensaje": "✅ PDF guardado exitosamente en MongoDB (Docker)",
        "datos": documento_guardado
    }