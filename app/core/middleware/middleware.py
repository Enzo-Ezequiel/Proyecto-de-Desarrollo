"""Middlewares HTTP de la aplicación."""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

# 1. Importamos nuestro logger centralizado
from app.core.utils import logger


class FileSizeLimitMiddleware:
    """Rechaza solicitudes HTTP cuyo `Content-Length` supera el límite configurado."""

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
                # 2. Registramos si alguien manda un header corrupto
                logger.warning("Se recibió un encabezado content-length con formato inválido.")

            if request_size is not None and request_size > self.max_size_bytes:
                # 3. Registramos una advertencia (warning) cuando se rechaza un archivo
                logger.warning(f"Solicitud HTTP rechazada: El tamaño ({request_size} bytes) excede el límite de {self.max_size_bytes} bytes.")
                
                limite_mb = self.max_size_bytes / (1024 * 1024)
                response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": f"El tamaño de la solicitud supera el límite permitido de {limite_mb:g}MB."
                    },
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)