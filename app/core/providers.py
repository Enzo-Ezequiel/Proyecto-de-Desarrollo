"""
Providers: Factory de dependencias para inyección con FastAPI.

Centraliza la creación de repositorios y servicios, evitando que
la Capa 3 (controladores) conozca implementaciones concretas.

NOTA para microservicios:
Cada microservicio redefiniría sus propios providers apuntando
a su BD y sus repositorios. Ejemplo:

    # pdf_service/providers.py
    def get_pdf_service():
        db = get_pdf_database()  # Apunta a la BD de PDFs
        repo = MongoRepository(db, "pdfs", DocumentoPDF)
        return PdfService(repo)
"""

from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.mongo_repository import MongoRepository
from app.models.pdf_document import DocumentoPDF
from app.services.pdf_service import PdfService


def get_pdf_service(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> PdfService:
    """FastAPI dependency: inyecta el servicio de PDFs con su repositorio."""
    repository = MongoRepository(
        db=db, collection_name="pdfs", entity_class=DocumentoPDF
    )
    return PdfService(repository)
