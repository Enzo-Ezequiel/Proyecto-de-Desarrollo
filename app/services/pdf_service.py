from app.schemas.pdf_schemas import PDFCreate
from app.core.mongo_repository import MongoRepository
from app.models.pdf_document import DocumentoPDF

# 👇 1. Importamos la función correcta (ya NO usamos 'db')
from app.core.database import get_database  

async def guardar_pdf(pdf_data: PDFCreate):
    """
    Toma los datos validados del controlador y los guarda en la base de datos.
    """
    # 👇 2. Instanciamos el repositorio AQUÍ ADENTRO para asegurar la conexión
    pdf_repo = MongoRepository(
        db=get_database(),            # Usamos tu función para obtener la BD
        entity_class=DocumentoPDF,    # Tu modelo de la Capa 1
        collection_name="pdfs"        # El nombre de la colección
    )
    
    # 3. Convertimos el esquema de Pydantic a un diccionario
    documento_dict = pdf_data.model_dump()
    
    # 4. Usamos tu repositorio para guardarlo en MongoDB
    resultado = await pdf_repo.create(documento_dict)
    
    return resultado