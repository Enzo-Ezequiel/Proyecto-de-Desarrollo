from app.models.base_model import BaseEntity

class DocumentoPDF(BaseEntity):
    def __init__(self, nombre_pdf: str, contenido_pdf: str, checksum: str, **kwargs):
        # 1. Ejecutamos el constructor del padre (BaseEntity) para que nos genere el ID y las fechas
        super().__init__(**kwargs)
        
        # 2. Guardamos los atributos propios del PDF
        self.nombre_pdf = nombre_pdf
        self.contenido_pdf = contenido_pdf
        self.checksum = checksum