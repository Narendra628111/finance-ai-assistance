"""
PDF document loader using PyMuPDF.

Supports:
- Digital PDFs
- Multi-page PDFs
- Metadata extraction
- Future OCR extension for scanned PDFs
"""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF

from backend.services.document.base_loader import BaseDocumentLoader
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class PDFLoader(BaseDocumentLoader):
    """
    PDF document loader.

    Extracts text from all pages of a PDF document.
    """

    def __init__(self, file_path: str | Path) -> None:
        super().__init__(file_path)

    async def load(self) -> str:
        """
        Extract text from the PDF.

        Returns:
            Extracted text.

        Raises:
            Exception:
                If PDF extraction fails.
        """
        self.validate()

        logger.info("Reading PDF: %s", self.file_path)

        try:
            document = fitz.open(self.file_path)

            pages: list[str] = []

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text").strip()

                if text:
                    pages.append(text)
                else:
                    logger.warning(
                        "No text found on page %d of %s",
                        page_number,
                        self.filename,
                    )

            document.close()

            extracted_text = "\n\n".join(pages).strip()

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(extracted_text),
                self.filename,
            )

            return extracted_text

        except Exception:
            logger.exception(
                "Failed to extract text from PDF '%s'.",
                self.filename,
            )
            raise

    def page_count(self) -> int:
        """
        Return the total number of pages.

        Returns:
            Number of pages.
        """
        self.validate()

        try:
            with fitz.open(self.file_path) as document:
                return document.page_count

        except Exception:
            logger.exception(
                "Unable to determine page count for '%s'.",
                self.filename,
            )
            raise

    def document_metadata(self) -> dict:
        """
        Return PDF metadata.

        Returns:
            Metadata dictionary.
        """
        self.validate()

        try:
            with fitz.open(self.file_path) as document:
                metadata = document.metadata or {}

            return {
                **super().metadata(),
                "page_count": self.page_count(),
                "title": metadata.get("title"),
                "author": metadata.get("author"),
                "subject": metadata.get("subject"),
                "keywords": metadata.get("keywords"),
                "creator": metadata.get("creator"),
                "producer": metadata.get("producer"),
                "creation_date": metadata.get("creationDate"),
                "modification_date": metadata.get("modDate"),
            }

        except Exception:
            logger.exception(
                "Unable to read metadata from '%s'.",
                self.filename,
            )
            raise