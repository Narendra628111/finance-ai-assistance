"""
Main entry point for the Finance AI Assistant backend.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from backend.api.routes.extractor import router as extractor_router
from backend.api.routes.summarizer import router as summarizer_router
from backend.config import settings
from backend.utils.logger import configure_logging, get_logger
from backend.core.exception_handlers import register_exception_handlers
from backend.api.routes.classifier import router as classifier_router
from backend.api.routes.vision import router as vision_router

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    """
    logger.info("%s is starting...", settings.APP_NAME)

    yield

    logger.info("%s is shutting down...", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(
    extractor_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    summarizer_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    classifier_router,
    prefix=settings.API_PREFIX,
)

app.include_router(
    vision_router,
    prefix="/api/v1",
)

@app.get(
    "/",
    tags=["Root"],
)
async def root() -> JSONResponse:
    """
    Root endpoint.
    """
    return JSONResponse(
        {
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "status": "running",
        }
    )


@app.get(
    "/health",
    tags=["Health"],
)
async def health() -> JSONResponse:
    """
    Health check endpoint.
    """
    return JSONResponse(
        {
            "status": "healthy",
            "application": settings.APP_NAME,
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )