"""
Application configuration module.

Loads and validates all application settings from environment variables.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# =============================================================================
# Paths
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# =============================================================================
# Settings
# =============================================================================

class Settings(BaseSettings):
    """
    Application settings.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # =========================================================================
    # Application
    # =========================================================================

    APP_NAME: str = "Finance AI Assistant"

    APP_VERSION: str = "1.0.0"

    APP_DESCRIPTION: str = (
        "A production-ready multimodal AI assistant "
        "for financial document analysis."
    )

    APP_ENV: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    DEBUG: bool = True

    # =========================================================================
    # API
    # =========================================================================

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    API_PREFIX: str = "/api/v1"

    # =========================================================================
    # LLM
    # =========================================================================

    LLM_PROVIDER: Literal[
        "groq",
        "gemini",
    ] = "groq"

    # =========================================================================
    # Groq
    # =========================================================================

    GROQ_API_KEY: str = Field(
        default="",
    )

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    GROQ_TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    GROQ_MAX_OUTPUT_TOKENS: int = Field(
        default=8192,
        gt=0,
    )

    # =========================================================================
    # Gemini - Optional fallback
    # =========================================================================

    GEMINI_API_KEY: str = Field(
        default="",
    )

    GEMINI_MODEL: str = "gemini-3-flash-preview"

    GEMINI_TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
    )

    GEMINI_MAX_OUTPUT_TOKENS: int = Field(
        default=8192,
        gt=0,
    )

    # =========================================================================
    # File Uploads
    # =========================================================================

    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024

    UPLOAD_DIR: Path = DATA_DIR / "uploads"

    SUPPORTED_DOCUMENT_TYPES: set[str] = {
        ".pdf",
        ".docx",
        ".txt",
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".tif",
        ".tiff",
    }

    # =========================================================================
    # RAG
    # =========================================================================

    POLICIES_DIR: Path = DATA_DIR / "policies"

    QDRANT_COLLECTION_NAME: str = "finance_knowledge"

    # Local embedding model.
    #
    # all-MiniLM-L6-v2 produces 384-dimensional vectors.
    # This removes the Gemini embedding dependency.
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    CHUNK_SIZE: int = 1000

    CHUNK_OVERLAP: int = 200

    TOP_K_RESULTS: int = 5

    QDRANT_PATH: Path = DATA_DIR / "vector_store"

    # all-MiniLM-L6-v2 -> 384 dimensions
    VECTOR_SIZE: int = 384

    SIMILARITY_THRESHOLD: float = 0.55

    # =========================================================================
    # Logging
    # =========================================================================

    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    LOG_DIR: Path = DATA_DIR / "logs"

    # =========================================================================
    # Future / Internal Directories
    # =========================================================================

    VECTOR_DB_DIR: Path = DATA_DIR / "vector_store"

    CACHE_DIR: Path = DATA_DIR / "cache"

    # =========================================================================
    # Directory Creation
    # =========================================================================

    @field_validator(
        "UPLOAD_DIR",
        "LOG_DIR",
        "VECTOR_DB_DIR",
        "CACHE_DIR",
        "POLICIES_DIR",
        "QDRANT_PATH",
        mode="after",
    )
    @classmethod
    def create_directories(
        cls,
        value: Path,
    ) -> Path:
        """
        Create required directories if they do not exist.
        """

        value.mkdir(
            parents=True,
            exist_ok=True,
        )

        return value


# =============================================================================
# Settings Factory
# =============================================================================

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()


# =============================================================================
# Global Settings
# =============================================================================

settings = get_settings()