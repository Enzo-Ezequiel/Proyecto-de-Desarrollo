"""Configuración de la aplicación FastAPI y centralizador de variables de entorno.

En una futura separación en microservicios, cada servicio cargará solo
las secciones que le correspondan (ver NOTA en cada bloque).
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación con variables de entorno.

    NOTA para microservicios:
    Cada microservicio debería tener su propia subclase de Settings
    cargando solo las variables que necesita. Ejemplo:
        class PdfServiceSettings(Settings):
            pdf_max_size_mb: int = 5
    """

    # ── App Info ──────────────────────────────────────────────────────────
    # Compartido por todos los servicios.
    app_name: str = "PDF Extractor"
    app_version: str = "0.1.0"
    app_description: str = "Aplicación FastAPI con arquitectura de tres capas siguiendo principios de Clean Code y Feature-Driven Development"

    # ── Server ────────────────────────────────────────────────────────────
    # Cada microservicio tendría su propio host/port.
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    # ── API Routing ───────────────────────────────────────────────────────
    # El prefix cambiaría por servicio: /api/v1/pdfs, /api/v1/users, etc.
    api_prefix: str = "/api/v1"
    api_docs_url: str = "/docs"
    api_redoc_url: str = "/redoc"

    # ── CORS ──────────────────────────────────────────────────────────────
    # Podría diferir entre servicios internos vs. externos.
    cors_origins: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    cors_allow_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_credentials: bool = True
    cors_allow_headers: List[str] = ["*"]

    # ── PDF Domain ────────────────────────────────────────────────────────
    # Solo aplica al microservicio de PDFs.
    pdf_max_size_mb: int = 5
    allowed_content_types: str = "application/pdf"

    # ── Logging ───────────────────────────────────────────────────────────
    # Compartido por todos los servicios.
    log_level: str = "INFO"

    # ── Backing Services (12-Factor) ──────────────────────────────────────
    # Cada microservicio apunta a su propia BD/cola.
    mongo_db_name: str
    database_url: str

    # Pydantic V2: lee el .env automáticamente
    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
