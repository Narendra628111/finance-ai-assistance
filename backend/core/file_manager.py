"""
Centralized file management utilities.
"""

from __future__ import annotations

import os
import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

from backend.config import settings
from backend.core.exception import (
    FileTooLargeError,
    UnsupportedFileTypeError,
)


class FileManager:
    """Handles upload validation, storage, and cleanup."""

    def __init__(
        self,
        upload_dir: Path | None = None,
        allowed_extensions: set[str] | None = None,
        max_file_size: int | None = None,
    ) -> None:
        self.upload_dir = upload_dir or settings.UPLOAD_DIR
        self.allowed_extensions = (
            allowed_extensions or settings.SUPPORTED_DOCUMENT_TYPES
        )
        self.max_file_size = (
            max_file_size or settings.MAX_UPLOAD_SIZE
        )

        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def validate_extension(self, filename: str) -> None:
        """Validate file extension."""

        extension = Path(filename).suffix.lower()

        if extension not in self.allowed_extensions:
            raise UnsupportedFileTypeError(
                f"Unsupported file type '{extension}'. "
                f"Allowed types: {', '.join(sorted(self.allowed_extensions))}"
            )

    async def validate_size(self, file: UploadFile) -> None:
        """Validate uploaded file size."""

        await file.seek(0, os.SEEK_END)
        size = file.file.tell()
        await file.seek(0)

        if size > self.max_file_size:
            raise FileTooLargeError(
                f"Maximum upload size is "
                f"{self.max_file_size / (1024 * 1024):.2f} MB."
            )

    @staticmethod
    def generate_filename(original_filename: str) -> str:
        """Generate a unique filename."""

        extension = Path(original_filename).suffix.lower()
        return f"{uuid.uuid4().hex}{extension}"

    async def save(self, file: UploadFile) -> Path:
        """
        Validate and save an uploaded file.

        Returns:
            Path of the saved file.
        """

        self.validate_extension(file.filename)

        await self.validate_size(file)

        filename = self.generate_filename(file.filename)

        destination = self.upload_dir / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await file.seek(0)

        return destination

    @staticmethod
    def delete(file_path: Path | str) -> None:
        """Delete a file if it exists."""

        path = Path(file_path)

        if path.exists():
            path.unlink()

    @staticmethod
    def exists(file_path: Path | str) -> bool:
        """Check if a file exists."""

        return Path(file_path).exists()

    @staticmethod
    def file_size(file_path: Path | str) -> int:
        """Return file size in bytes."""

        return Path(file_path).stat().st_size