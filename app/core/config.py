"""
Configuración de la aplicación FastAPI.

Gestiona las variables de entorno y la configuración global.
Principios aplicados:
- Single Responsibility: Solo maneja configuración.
- DRY: Centraliza todas las configuraciones.
"""

from typing import Optional

from pydantic_settings import BaseSettings

# ============================================================================
# Configuration Constants - Valores por defecto y constantes de configuración
# ============================================================================

# Información de la aplicación
APP_NAME = "Repositorio Desarrollo"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = (
    "Aplicación FastAPI con arquitectura de tres capas "
    "siguiendo principios de Clean Code y Feature-Driven Development"
)

# Configuración del servidor
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DEFAULT_DEBUG = False

# Configuración de la API
API_PREFIX = "/api/v1"
API_DOCS_URL = "/docs"
API_REDOC_URL = "/redoc"

# Configuración de CORS
DEFAULT_CORS_ORIGINS = ["http://localhost", "http://localhost:3000"]
DEFAULT_CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
DEFAULT_CORS_ALLOW_CREDENTIALS = True
DEFAULT_CORS_ALLOW_HEADERS = ["*"]


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Todas las configuraciones se pueden establecer mediante variables de entorno.
    Los valores por defecto están definidos como constantes para reutilización.
    """

    # Información de la aplicación
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    app_description: str = APP_DESCRIPTION

    # Configuración del servidor
    debug: bool = DEFAULT_DEBUG
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    # Configuración de la API
    api_prefix: str = API_PREFIX
    api_docs_url: str = API_DOCS_URL
    api_redoc_url: str = API_REDOC_URL

    # Configuración de CORS
    cors_origins: list[str] = DEFAULT_CORS_ORIGINS
    cors_allow_credentials: bool = DEFAULT_CORS_ALLOW_CREDENTIALS
    cors_allow_methods: list[str] = DEFAULT_CORS_ALLOW_METHODS
    cors_allow_headers: list[str] = DEFAULT_CORS_ALLOW_HEADERS

    # Base de datos
    database_url: str = "mongodb://localhost:27017"
    mongo_db_name: str = "repositorio_db"

    class Config:
        """Configuración de Pydantic Settings."""

        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
