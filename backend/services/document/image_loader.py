"""
Image document loader using Google Gemini Vision.

Supports:
- PNG
- JPG
- JPEG
- WEBP
- BMP
- TIFF

Uses Gemini Vision to extract text and understand image content.
"""

from __future__ import annotations

from pathlib import Path

from backend.services.document.base_loader import BaseDocumentLoader
from backend.services.llm.gemini_service import GeminiService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ImageLoader(BaseDocumentLoader):
    """
    Loader for image documents.

    Extracts all readable text while preserving the document structure.
    """

    MIME_TYPES = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }

    EXTRACTION_PROMPT = """
You are an expert OCR and document understanding assistant.

Your task is to extract every piece of readable text from the image.

Instructions:
- Preserve headings.
- Preserve paragraphs.
- Preserve tables whenever possible.
- Preserve bullet points.
- Do not summarize.
- Do not explain.
- Do not hallucinate.
- Return only the extracted text.
"""

    def __init__(self, file_path: str | Path) -> None:
        super().__init__(file_path)
        self.llm = GeminiService()

    async def load(self) -> str:
        """
        Extract text from an image using Gemini Vision.

        Returns:
            Extracted text.

        Raises:
            ValueError:
                If image type is unsupported.
        """
        self.validate()

        extension = self.extension.lower()

        if extension not in self.MIME_TYPES:
            raise ValueError(
                f"Unsupported image format: {extension}"
            )

        logger.info("Reading image: %s", self.file_path)

        try:
            with open(self.file_path, "rb") as image_file:
                image_bytes = image_file.read()

            extracted_text = await self.llm.generate_from_image(
                image_bytes=image_bytes,
                mime_type=self.MIME_TYPES[extension],
                prompt=self.EXTRACTION_PROMPT,
            )

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(extracted_text),
                self.filename,
            )

            return extracted_text.strip()

        except Exception:
            logger.exception(
                "Failed to extract text from image '%s'.",
                self.filename,
            )
            raise

    def document_metadata(self) -> dict:
        """
        Return image metadata.

        Returns:
            Metadata dictionary.
        """
        metadata = super().metadata()

        metadata["mime_type"] = self.MIME_TYPES.get(
            self.extension.lower(),
            "application/octet-stream",
        )

        return metadata