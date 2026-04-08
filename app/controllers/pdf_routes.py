from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService
import shutil
import os

# Definición del router para operaciones relacionadas con archivos PDF
router = APIRouter(prefix="/pdf", tags=["PDF Operations"])

# Instanciamos los servicios (Inyección de dependencias simplificada)
pdf_service = PDFService()
ai_service = AIService()

@router.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    """
    Endpoint para cargar un archivo PDF, extraer su texto y generar un resumen mediante IA.

    Args:
        file (UploadFile): Archivo PDF enviado a través de un formulario multipart/form-data.

    Returns:
        dict: Un diccionario con el nombre del archivo y el resumen generado.
    """
    
    # 1. Gestión de archivos temporales
    # Se crea un archivo local para procesar el contenido binario del PDF
    temp_path = f"temp_{file.filename}"
    
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Extracción de información
        # Delegamos la responsabilidad de lectura al PDFService (SRP)
        text = pdf_service.extract_text(temp_path)
        
        if not text:
            raise ValueError("No se pudo extraer texto del archivo.")
        
        # 3. Generación de conocimiento
        # El AIService se encarga de la lógica de negocio del resumen
        summary = ai_service.summarize_content(text)
        
        return {
            "filename": file.filename,
            "summary": summary
        }

    except Exception as e:
        # Manejo de errores para mantener la robustez del sistema
        raise HTTPException(status_code=500, detail=f"Error procesando el PDF: {str(e)}")
    
    finally:
        # 4. Limpieza del entorno (Seiso)
        # Se garantiza la eliminación del archivo temporal incluso si ocurre un error
        if os.path.exists(temp_path):
            os.remove(temp_path)