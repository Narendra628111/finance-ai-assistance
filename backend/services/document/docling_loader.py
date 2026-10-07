"""
Generic document loader using Docling.
"""

from __future__ import annotations

from pathlib import Path

from backend.services.document.base_loader import BaseDocumentLoader
from backend.services.document.docling_service import DoclingService
from backend.utils.logger import get_logger


logger = get_logger(__name__)


class DoclingLoader(BaseDocumentLoader):
    """
    Generic document loader.

    Uses Docling for:
    - PDF
    - DOCX
    - TXT
    - PNG
    - JPG/JPEG
    - BMP
    - TIFF
    - WEBP
    """

    def __init__(
        self,
        file_path: str | Path,
    ) -> None:
        super().__init__(file_path)

        self.docling = DoclingService()

    async def load(self) -> str:
        """
        Extract text from the document using Docling.
        """

        self.validate()

        logger.info(
            "Reading document using Docling: %s",
            self.file_path,
        )

        text = await self.docling.extract(
            self.file_path,
        )

        if not text or not text.strip():
            raise ValueError(
                f"No text could be extracted from "
                f"'{self.filename}'."
            )

        logger.info(
            "Successfully extracted %d characters "
            "from '%s'.",
            len(text),
            self.filename,
        )

        return text.strip()

    def document_metadata(self) -> dict:
        """
        Return document metadata.
        """

        metadata = super().metadata()

        metadata["type"] = self.file_path.suffix.lower().replace(
            ".",
            "",
        )

        return metadata