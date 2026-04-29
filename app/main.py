"""
Punto de entrada de la aplicación FastAPI.

Inicializa la aplicación FastAPI con:
- Configuración global
- Routers de controladores
- Middleware CORS
- Documentación automática

Principios aplicados:
- Single Responsibility: Solo configura y monta la app.
- Inyección de dependencias: Las dependencias vienen de FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core import settings
from app.core.database import close_connection

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
    debug=settings.debug,
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    """
    Endpoint raíz para verificar que la aplicación está funcionando.

    Returns:
        Mensaje de bienvenida.
    """
    return {"message": f"Bienvenido a {settings.app_name} v{settings.app_version}"}


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """
    Endpoint de verificación de salud (health check).

    Returns:
        Estado de salud de la aplicación.
    """
    return {"status": "ok", "message": "Aplicación funcionando correctamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )
