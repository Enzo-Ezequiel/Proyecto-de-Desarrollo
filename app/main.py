from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos las configuraciones y la base de datos
from app.core import settings
from app.core.database import connect_to_mongo, close_mongo_connection

# Importamos nuestro nuevo controlador
from app.controllers.user_routes import router as user_router

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
    redoc_url=settings.api_redoc_url
)

# Configuramos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Registramos nuestras rutas (Controladores)
app.include_router(user_router, prefix=settings.api_prefix)

@app.get("/")
async def root():
    return {"mensaje": f"Bienvenido a {settings.app_name} - API Activa"}