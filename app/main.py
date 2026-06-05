from contextlib import asynccontextmanager

# Limpiamos los imports que ya no se usan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.pdf_routes import router as pdf_router

# Configuración y base de datos (Importamos explícitamente config)
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.middleware.middleware import FileSizeLimitMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio
    await connect_to_mongo()
    yield
    # Cierre
    await close_mongo_connection()

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# 12-Factor App: Usamos la configuración de tu .env en lugar de un número hardcodeado
app.add_middleware(
    FileSizeLimitMiddleware, 
    max_size_bytes=settings.pdf_max_size_mb * 1024 * 1024
)

# Rutas: ¡Solo enchufamos los PDFs para cumplir estrictamente con la Etapa 1!
app.include_router(pdf_router)