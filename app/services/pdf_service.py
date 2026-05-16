import io
import hashlib
import pypdf
from fastapi import UploadFile

from app.core.mongo_repository import MongoRepository
from app.models.pdf_document import DocumentoPDF
from app.core.database import get_database


async def procesar_y_guardar_pdf(file: UploadFile):
    """Procesa el PDF en memoria, valida duplicados mediante checksum y persiste la entidad en MongoDB."""
    # Instancia el repositorio
    pdf_repo = MongoRepository(
        db=get_database(), entity_class=DocumentoPDF, collection_name="pdfs"
    )

    # Lee el contenido
    contenido_bytes = await file.read()

    # Valida el tamaño
    limite_mb = 5
    if len(contenido_bytes) > (limite_mb * 1024 * 1024):
        raise ValueError(
            f"El archivo excede el tamaño máximo permitido de {limite_mb}MB."
        )

    # Genera checksum
    checksum = hashlib.sha256(contenido_bytes).hexdigest()

    # Verifica duplicados
    pdf_duplicado = await pdf_repo.collection.find_one({"checksum": checksum})
    if pdf_duplicado:
        raise ValueError(
            "Este documento PDF ya existe en la base de datos. No se permiten duplicados."
        )

    # Extrae texto del PDF
    texto_extraido = ""
    lector_pdf = pypdf.PdfReader(io.BytesIO(contenido_bytes))

    for pagina in lector_pdf.pages:
        texto = pagina.extract_text()
        if texto:
            texto_extraido += texto + "\n"

    # Crea entidad del dominio
    nuevo_documento = DocumentoPDF(
        nombre_pdf=file.filename,
        contenido_pdf=texto_extraido.strip(),
        checksum=checksum,
    )

    # Persiste en MongoDB
    resultado = await pdf_repo.add(nuevo_documento)

    return resultado


async def obtener_todos_los_pdfs():
    """Obtiene todos los PDFs guardados en la base de datos."""
    pdf_repo = MongoRepository(
        db=get_database(), entity_class=DocumentoPDF, collection_name="pdfs"
    )
    return await pdf_repo.get_all()


async def obtener_pdf_por_id(pdf_id: str):
    """Busca un PDF específico por su ID."""
    pdf_repo = MongoRepository(
        db=get_database(), entity_class=DocumentoPDF, collection_name="pdfs"
    )
    return await pdf_repo.get_by_id(pdf_id)


async def eliminar_pdf(pdf_id: str):
    """Elimina un PDF de la base de datos usando su ID."""
    pdf_repo = MongoRepository(
        db=get_database(), entity_class=DocumentoPDF, collection_name="pdfs"
    )
    return await pdf_repo.delete(pdf_id)
