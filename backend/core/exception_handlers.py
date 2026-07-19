"""
Global exception handlers.
"""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.core.exception import (
    AIAssistantError,
    ConfigurationError,
    DocumentError,
    ExtractionError,
    LLMError,
    ValidationError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(ConfigurationError)
    async def configuration_exception_handler(
        request: Request,
        exc: ConfigurationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(DocumentError)
    async def document_exception_handler(
        request: Request,
        exc: DocumentError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(LLMError)
    async def llm_exception_handler(
        request: Request,
        exc: LLMError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(ExtractionError)
    async def extraction_exception_handler(
        request: Request,
        exc: ExtractionError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(AIAssistantError)
    async def ai_assistant_exception_handler(
        request: Request,
        exc: AIAssistantError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": exc.message,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Internal Server Error",
            },
        )