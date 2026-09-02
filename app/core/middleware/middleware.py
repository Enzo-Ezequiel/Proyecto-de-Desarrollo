"""Middlewares HTTP de la app."""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.utils import logger


class FileSizeLimitMiddleware:
    """Rechaza peticiones con Content-Length mayor al límite, sin leer el cuerpo.

    Primera capa de una defensa en profundidad sobre el mismo límite de tamaño:

    - Acá (capa HTTP): se mira solo el header ``Content-Length`` y se corta con
      ``413`` antes de leer el body. Filtro barato y temprano contra subidas
      grandes.
    - En ``PdfService._validar_tamano`` (capa de negocio): se mide el tamaño real
      del contenido ya leído y se responde ``400``. Hace falta porque el header
      puede faltar o mentir, así que el middleware no alcanza como única barrera.

    Los status difieren a propósito: ``413`` = "ni mandes esto"; ``400`` = "recibí
    el archivo y no cumple la regla de negocio".
    """

    def __init__(self, app: ASGIApp, max_size_bytes: int = 10 * 1024 * 1024) -> None:
        self.app = app
        self.max_size_bytes = max_size_bytes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        content_length = headers.get(b"content-length")

        if content_length is not None:
            try:
                request_size = int(content_length.decode("latin-1"))
            except ValueError:
                request_size = None
                logger.warning("Header content-length malformado")

            if request_size is not None and request_size > self.max_size_bytes:
                logger.warning(
                    f"Petición rechazada: {request_size} bytes > límite {self.max_size_bytes} bytes"
                )

                limite_mb = self.max_size_bytes / (1024 * 1024)
                response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": f"Tamaño de petición supera el límite de {limite_mb:g}MB."
                    },
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
