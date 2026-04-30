from app.models.base_model import BaseEntity

class DocumentoPDF(BaseEntity):
    nombre_pdf: str          
    contenido_pdf: str       
    checksum: str     