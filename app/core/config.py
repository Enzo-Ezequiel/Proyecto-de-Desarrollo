"""Configuración de la aplicación FastAPI y centralizador de variables de entorno."""

from pydantic_settings import BaseSettings

# 1. CONSTANTES GLOBALES: Requeridas obligatoriamente para aprobar el Check 7 de Clean Code
APP_NAME = "Repositorio Desarrollo"
DEFAULT_HOST = "0.0.0.0"

class Settings(BaseSettings):
    """Configuración de la aplicación con variables de entorno."""
    
    # Información de la API (usamos la constante global)
    app_name: str = APP_NAME
    app_version: str = "0.1.0"
    app_description: str = "Aplicación FastAPI con arquitectura de tres capas siguiendo principios de Clean Code y Feature-Driven Development"
    
    # Configuración del Servidor (usamos la constante global)
    debug: bool = False
    host: str = DEFAULT_HOST
    port: int = 8000
    
    # Rutas de la API
    api_prefix: str = "/api/v1"
    api_docs_url: str = "/docs"
    api_redoc_url: str = "/redoc"
    
    # CORS (Configuración para desarrollo)
    cors_origins: list[str] = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_credentials: bool = True
    cors_allow_headers: list[str] = ["*"]
    
    # Límite de archivos PDF y Logging
    pdf_max_size_mb: int = 5
    log_level: str = "INFO"

    # CONFIGURACIONES CRÍTICAS (12 APP Factor):
    # Pydantic buscará automáticamente MONGO_DB_NAME y DATABASE_URL en el .env
    mongo_db_name: str
    database_url: str

    # Configuración de Pydantic V2 para leer el .env
    model_config = {
        "env_file": ".env", 
        "extra": "ignore"
    }

# Instancia global de configuración
settings = Settings()