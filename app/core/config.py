"""Configuración de la aplicación FastAPI."""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Configuración de la aplicación con variables de entorno."""
    
    # Información de la API (pueden tener valores por defecto)
    APP_NAME: str = "Repositorio Desarrollo"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Aplicación FastAPI con arquitectura de tres capas siguiendo principios de Clean Code y Feature-Driven Development"
    
    # Configuración del Servidor
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Rutas de la API
    API_PREFIX: str = "/api/v1"
    API_DOCS_URL: str = "/docs"
    API_REDOC_URL: str = "/redoc"
    
    # CORS (Configuración para desarrollo)
    CORS_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Límite de archivos PDF y Logging
    PDF_MAX_SIZE_MB: int = 5
    LOG_LEVEL: str = "INFO"

    # CONFIGURACIONES CRÍTICAS (12 APP Factor):
    # Solo se declara el tipo, Pydantic leerá el valor real desde el archivo .env
    MONGO_DB_NAME: str
    DATABASE_URL: str

    model_config = {
        "env_file": ".env", 
        "extra": "ignore"
    }

# Instancia global de configuración
settings = Settings()
