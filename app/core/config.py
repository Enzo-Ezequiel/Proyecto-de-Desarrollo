"""Configuración FastAPI + variables de entorno (.env)."""

from pydantic_settings import BaseSettings

# Constantes globales (requeridas por Clean Code check)
APP_NAME = "Repositorio Desarrollo"
DEFAULT_HOST = "0.0.0.0"


class Settings(BaseSettings):
    """Settings de la app desde variables de entorno."""

    # Info API
    app_name: str = APP_NAME
    app_version: str = "0.1.0"
    app_description: str = (
        "FastAPI 3-layer architecture, Clean Code + Feature-Driven Development"
    )

    # Servidor
    debug: bool = False
    host: str = DEFAULT_HOST
    port: int = 8000

    # Rutas API
    api_prefix: str = "/api/v1"
    api_docs_url: str = "/docs"
    api_redoc_url: str = "/redoc"

    # CORS (dev)
    cors_origins: list[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_credentials: bool = True
    cors_allow_headers: list[str] = ["*"]

    # Límites y logging
    pdf_max_size_mb: int = 5
    log_level: str = "INFO"

    # 12-Factor App: obligatorias desde .env
    mongo_db_name: str
    database_url: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
