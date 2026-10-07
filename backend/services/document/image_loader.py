"""
Image document loader using Docling OCR.
"""

from __future__ import annotations

from pathlib import Path

from backend.services.document.base_loader import BaseDocumentLoader
from backend.services.document.docling_service import DoclingService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ImageLoader(BaseDocumentLoader):
    """
    Image loader powered by Docling OCR.

    Supports:
    - PNG
    - JPG
    - JPEG
    - WEBP
    - BMP
    - TIFF
    """

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".tif",
        ".tiff",
    }

    def __init__(
        self,
        file_path: str | Path,
    ) -> None:
        super().__init__(file_path)
        self.docling = DoclingService()

    async def load(self) -> str:
        """
        Extract text from an image using Docling.
        """

        self.validate()

        if self.extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported image format: {self.extension}"
            )

        logger.info(
            "Reading image: %s",
            self.file_path,
        )

        text = await self.docling.extract(
            self.file_path,
        )

        logger.info(
            "Successfully extracted %d characters from '%s'.",
            len(text),
            self.filename,
        )

        return text

    def document_metadata(self) -> dict:

        metadata = super().metadata()

        metadata["type"] = "image"

        return metadata