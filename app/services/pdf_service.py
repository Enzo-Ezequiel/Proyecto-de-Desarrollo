import io
import hashlib
import PyPDF2
from fastapi import UploadFile

from app.core.mongo_repository import MongoRepository
from app.models.pdf_document import DocumentoPDF
from app.core.database import get_database

async def procesar_y_guardar_pdf(file: UploadFile):
    """
    Recibe un archivo, lo procesa en memoria (sin guardarlo en disco), 
    extrae su texto, verifica duplicados y lo guarda en la BD.
    """
    # 1. Instanciamos el repositorio
    pdf_repo = MongoRepository(
        db=get_database(),
        entity_class=DocumentoPDF,
        collection_name="pdfs"
    )
    
    # 2. Leer el archivo en memoria RAM
    contenido_bytes = await file.read()
    
    # 3. Validación de Tamaño (Límite de 5 Megabytes)
    limite_mb = 5
    if len(contenido_bytes) > (limite_mb * 1024 * 1024):
        raise ValueError(f"El archivo excede el tamaño máximo permitido de {limite_mb}MB.")

    # 4. Generar el Checksum (SHA-256)
    checksum = hashlib.sha256(contenido_bytes).hexdigest()

    # 5. Validación de Duplicados
    # Buscamos en la base de datos si ya existe un documento con esta huella digital
    pdf_duplicado = await pdf_repo.collection.find_one({"checksum": checksum})
    if pdf_duplicado:
        raise ValueError("Este documento PDF ya existe en la base de datos. No se permiten duplicados.")
    
    # 6. Extraer el texto usando PyPDF2 directamente desde la memoria
    texto_extraido = ""
    lector_pdf = PyPDF2.PdfReader(io.BytesIO(contenido_bytes))
    
    for pagina in lector_pdf.pages:
        texto = pagina.extract_text()
        if texto:
            texto_extraido += texto + "\n"

    # 7. Instanciamos tu Entidad de Dominio (Capa 1)
    nuevo_documento = DocumentoPDF(
        nombre_pdf=file.filename,
        contenido_pdf=texto_extraido.strip(),
        checksum=checksum
    )
    
    # 8. Guardar en MongoDB usando el método "add"
    resultado = await pdf_repo.add(nuevo_documento)
    
    return resultado

async def obtener_todos_los_pdfs():
    """Obtiene todos los PDFs guardados en la base de datos."""
    pdf_repo = MongoRepository(
        db=get_database(),
        entity_class=DocumentoPDF,
        collection_name="pdfs"
    )
    return await pdf_repo.get_all()

async def obtener_pdf_por_id(pdf_id: str):
    """Busca un PDF específico por su ID."""
    pdf_repo = MongoRepository(
        db=get_database(),
        entity_class=DocumentoPDF,
        collection_name="pdfs"
    )
    return await pdf_repo.get_by_id(pdf_id)

async def eliminar_pdf(pdf_id: str):
    """Elimina un PDF de la base de datos usando su ID."""
    pdf_repo = MongoRepository(
        db=get_database(),
        entity_class=DocumentoPDF,
        collection_name="pdfs"
    )
    return await pdf_repo.delete(pdf_id)