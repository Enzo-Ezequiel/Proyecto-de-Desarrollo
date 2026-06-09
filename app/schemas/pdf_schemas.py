from typing import Optional
from pydantic import BaseModel

# Este esquema valida estrictamente los datos que recibiremos al CREAR un PDF
class PDFCreate(BaseModel):
    nombre_pdf: str
    contenido_pdf: str
    checksum: str

# Esquema que valida los datos al ACTUALIZAR un PDF
class PDFUpdate(BaseModel):
    nombre_pdf: Optional[str] = None
    contenido_pdf: Optional[str] = None