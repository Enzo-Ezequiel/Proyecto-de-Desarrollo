from pydantic import BaseModel

# Este esquema valida estrictamente los datos que recibiremos en la petición HTTP
class PDFCreate(BaseModel):
    nombre_pdf: str
    contenido_pdf: str
    checksum: str