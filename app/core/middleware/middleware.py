"""Middlewares HTTP de la aplicación."""

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


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

            if request_size is not None and request_size > self.max_size_bytes:
                response = JSONResponse(
                    status_code=413,
                    content={
                        "detail": "El tamaño de la solicitud supera el límite permitido de 10MB."
                    },
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
