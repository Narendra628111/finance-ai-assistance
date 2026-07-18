"""
Application logging configuration.

Provides a centralized logger for the entire application.
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path

from backend.config import settings


LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _create_console_handler() -> logging.StreamHandler:
    """Create and configure console log handler."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    return handler


def _create_file_handler(log_file: Path) -> logging.Handler:
    """Create and configure rotating file log handler."""
    handler = logging.handlers.RotatingFileHandler(
        filename=log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    handler.setLevel(settings.LOG_LEVEL)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    return handler


def configure_logging() -> None:
    """
    Configure application-wide logging.

    This should be called once during application startup.
    """
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(settings.LOG_LEVEL)

    log_file = settings.LOG_DIR / "application.log"

    root_logger.addHandler(_create_console_handler())
    root_logger.addHandler(_create_file_handler(log_file))


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance.
    """
    configure_logging()
    return logging.getLogger(name)