"""
Abstract base class for all document loaders.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseDocumentLoader(ABC):
    """
    Base interface for all document loaders.

    Every document loader (PDF, DOCX, TXT, Image, etc.)
    must inherit from this class.
    """

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    @property
    def filename(self) -> str:
        """Return file name."""
        return self.file_path.name

    @property
    def extension(self) -> str:
        """Return file extension."""
        return self.file_path.suffix.lower()

    @property
    def exists(self) -> bool:
        """Check whether file exists."""
        return self.file_path.exists()

    def validate(self) -> None:
        """
        Validate input file.

        Raises:
            FileNotFoundError:
                If the file does not exist.

            ValueError:
                If the path is not a file.
        """
        if not self.exists:
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        if not self.file_path.is_file():
            raise ValueError(
                f"Invalid file path: {self.file_path}"
            )

    @abstractmethod
    async def load(self) -> str:
        """
        Extract text from the document.

        Returns:
            Extracted text.
        """
        raise NotImplementedError

    def metadata(self) -> dict[str, Any]:
        """
        Return basic file metadata.

        Returns:
            Dictionary containing file metadata.
        """
        stats = self.file_path.stat()

        return {
            "filename": self.filename,
            "path": str(self.file_path.resolve()),
            "extension": self.extension,
            "size_bytes": stats.st_size,
            "created_at": stats.st_ctime,
            "modified_at": stats.st_mtime,
        }