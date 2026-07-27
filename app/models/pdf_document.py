from app.models.base_model import BaseEntity


class DocumentoPDF(BaseEntity):
    def __init__(self, nombre_pdf: str, contenido_pdf: str, checksum: str, **kwargs):
        # Primero llamamos al padre para que genere ID y fechas
        super().__init__(**kwargs)

        # Guardamos lo propio del PDF
        self.nombre_pdf = nombre_pdf
        self.contenido_pdf = contenido_pdf
        self.checksum = checksum
