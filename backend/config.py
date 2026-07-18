"""
Application configuration module.

Loads and validates all application settings from environment variables.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"

LLM_PROVIDER: str = "gemini"
class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ==========================================================================
    # Application
    # ==========================================================================

    APP_NAME: str = "Finance AI Assistant"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "A production-ready multimodal AI assistant for financial document analysis."
    )
    APP_ENV: Literal["development", "testing", "staging", "production"] = (
        "development"
    )
    DEBUG: bool = True

    # ==========================================================================
    # API
    # ==========================================================================

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"

    # ==========================================================================
    # Gemini
    # ==========================================================================

    GEMINI_API_KEY: str = Field(..., min_length=1)
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = Field(default=0.2, ge=0.0, le=2.0)
    GEMINI_MAX_OUTPUT_TOKENS: int = Field(default=8192, gt=0)

    # ==========================================================================
    # File Uploads
    # ==========================================================================

    MAX_UPLOAD_SIZE: int = 20 * 1024 * 1024
    UPLOAD_DIR: Path = DATA_DIR / "uploads"

    SUPPORTED_DOCUMENT_TYPES: set[str] = {
    ".pdf",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    }

    # ==========================================================================
    # Logging
    # ==========================================================================

    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"

    LOG_DIR: Path = DATA_DIR / "logs"

    # ==========================================================================
    # Future Extensions
    # ==========================================================================

    VECTOR_DB_DIR: Path = DATA_DIR / "vector_store"
    CACHE_DIR: Path = DATA_DIR / "cache"

    @field_validator(
        "UPLOAD_DIR",
        "LOG_DIR",
        "VECTOR_DB_DIR",
        "CACHE_DIR",
        mode="after",
    )
    @classmethod
    def create_directories(cls, value: Path) -> Path:
        """Create directories if they don't exist."""
        value.mkdir(parents=True, exist_ok=True)
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()