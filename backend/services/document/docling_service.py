"""
Unified document extraction service using Docling
with RapidOCR fallback for images.
"""

from __future__ import annotations

import re
from pathlib import Path

from docling.document_converter import DocumentConverter
from rapidocr import RapidOCR

from backend.utils.logger import get_logger


logger = get_logger(__name__)


# -------------------------------------------------------------------------
# Shared instances
# -------------------------------------------------------------------------

# One Docling converter for the application.
_converter = DocumentConverter()

# One RapidOCR engine for the application.
_ocr_engine = RapidOCR()


class DoclingService:
    """
    Service responsible for extracting text from:

    - PDF
    - DOCX
    - TXT
    - PNG
    - JPG
    - JPEG
    - BMP
    - WEBP
    - TIFF

    Docling is used first.

    For images, if Docling returns no useful text,
    RapidOCR is used as a fallback.
    """

    def __init__(self) -> None:
        self.converter = _converter
        self.ocr = _ocr_engine

    async def extract(
        self,
        file_path: str | Path,
    ) -> str:
        """
        Extract text from a document.

        Docling is attempted first.

        If the input is an image and Docling does not
        return useful text, RapidOCR is used as fallback.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        logger.info(
            "Extracting document using Docling: %s",
            path.name,
        )

        # -------------------------------------------------------------
        # 1. Try Docling
        # -------------------------------------------------------------

        try:

            result = self.converter.convert(path)

            text = result.document.export_to_markdown()

            # Remove Docling image placeholders.
            text = re.sub(
                r"<!--.*?-->",
                "",
                text,
                flags=re.DOTALL,
            )

            # Remove excessive blank lines.
            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text,
            )

            text = text.strip()

            logger.info(
                "Docling extracted %d characters from '%s'.",
                len(text),
                path.name,
            )

            # ---------------------------------------------------------
            # If Docling successfully extracted text, return it.
            # ---------------------------------------------------------

            if text:
                return text

            logger.warning(
                "Docling returned empty text for '%s'.",
                path.name,
            )

        except Exception:
            logger.exception(
                "Docling extraction failed for '%s'.",
                path.name,
            )

            # For non-image documents, do not silently hide the error.
            if not self._is_image(path):
                raise

        # -------------------------------------------------------------
        # 2. RapidOCR fallback for images
        # -------------------------------------------------------------

        if self._is_image(path):

            logger.info(
                "Trying RapidOCR fallback for '%s'.",
                path.name,
            )

            try:

                text = await self._extract_with_ocr(path)

                if text:
                    logger.info(
                        "RapidOCR extracted %d characters from '%s'.",
                        len(text),
                        path.name,
                    )

                    return text

            except Exception:
                logger.exception(
                    "RapidOCR fallback failed for '%s'.",
                    path.name,
                )

        # -------------------------------------------------------------
        # 3. Nothing worked
        # -------------------------------------------------------------

        raise ValueError(
            f"No text could be extracted from '{path.name}'."
        )

    async def _extract_with_ocr(
        self,
        path: Path,
    ) -> str:
        """
        Extract text directly using RapidOCR.
        """

        import asyncio

        result = await asyncio.to_thread(
            self.ocr,
            str(path),
        )

        # RapidOCR normally returns a RapidOCROutput
        # containing `txts`.
        txts = getattr(
            result,
            "txts",
            None,
        )

        if not txts:
            logger.warning(
                "RapidOCR returned no text for '%s'.",
                path.name,
            )

            return ""

        # -------------------------------------------------------------
        # Clean individual OCR results
        # -------------------------------------------------------------

        lines = []

        for text in txts:

            if text is None:
                continue

            text = str(text).strip()

            if not text:
                continue

            lines.append(text)

        # -------------------------------------------------------------
        # Preserve each OCR result as a separate line.
        # -------------------------------------------------------------

        return "\n".join(lines).strip()

    @staticmethod
    def _is_image(
        path: Path,
    ) -> bool:
        """
        Check whether a file is an image.
        """

        return path.suffix.lower() in {
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".webp",
            ".tif",
            ".tiff",
        }