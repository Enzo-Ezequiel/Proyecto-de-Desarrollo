from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.controllers.pdf_routes import router as pdf_router

# Importamos nuestros controladores
from app.controllers.user_routes import router as user_router

# Importamos las configuraciones y la base de datos
from app.core import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.middleware.middleware import FileSizeLimitMiddleware


# Configuramos el ciclo de vida de la app para la Base de Datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Esto se ejecuta justo al iniciar el servidor
    await connect_to_mongo()
    yield
    # Esto se ejecuta al apagar el servidor
    await close_mongo_connection()


# Creamos la aplicación inyectando el lifespan
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
)

# Configuramos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.add_middleware(FileSizeLimitMiddleware, max_size_bytes=10 * 1024 * 1024)

# Registramos nuestras rutas (Controladores)
app.include_router(user_router, prefix=settings.api_prefix)
app.include_router(pdf_router)


@app.get("/")
async def root():
    return {"mensaje": f"Bienvenido a {settings.app_name} - API Activa"}


@app.post("/test-upload")
async def test_upload(file: UploadFile = File(...)):
    contenido = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contenido),
    }
