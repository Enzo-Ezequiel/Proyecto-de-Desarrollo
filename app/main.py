from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.controllers.pdf_routes import router as pdf_router
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.exceptions import AppException
from app.core.middleware.middleware import FileSizeLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url=settings.api_docs_url,
    redoc_url=settings.api_redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

app.add_middleware(
    FileSizeLimitMiddleware, max_size_bytes=settings.pdf_max_size_mb * 1024 * 1024
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Traduce las excepciones de dominio a respuestas HTTP consistentes."""
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


app.include_router(pdf_router)
