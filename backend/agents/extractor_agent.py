"""
Generic Extractor Agent.

Responsibilities:
- Select the appropriate document loader.
- Extract document text.
- Build extraction prompt.
- Invoke the LLM.
- Parse and validate the response.
- Return a standardized extraction response.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.models.extraction_models import (
    ExtractionRequest,
    ExtractionResponse,
    ExtractionResult,
)
from backend.prompts.extraction_prompt import ExtractionPrompt
from backend.services.document.loader_factory import LoaderFactory
from backend.services.extraction.response_parser import ResponseParser
from backend.services.llm.gemini_service import GeminiService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ExtractorAgent:
    """
    Generic document extraction agent.
    """

    def __init__(
        self,
        llm: GeminiService | None = None,
    ) -> None:
        self.llm = llm or GeminiService()

    async def extract(
        self,
        file_path: str | Path,
        schema: dict[str, Any],
        instructions: str | None = None,
    ) -> ExtractionResponse:
        """
        Extract structured information from a document.

        Args:
            file_path:
                Document path.

            schema:
                Expected output schema.

            instructions:
                Additional extraction instructions.

        Returns:
            ExtractionResponse
        """

        file_path = Path(file_path)

        logger.info("Starting extraction for %s", file_path.name)

        try:
            # --------------------------------------------------------
            # Select appropriate loader
            # --------------------------------------------------------

            loader = LoaderFactory.get_loader(file_path)

            logger.info(
                "Using %s",
                loader.__class__.__name__,
            )

            # --------------------------------------------------------
            # Extract text
            # --------------------------------------------------------

            document_text = await loader.load()

            if not document_text.strip():
                raise ValueError(
                    "No text could be extracted from the document."
                )

            metadata = loader.document_metadata()

            logger.info(
                "Extracted %d characters.",
                len(document_text),
            )

            # --------------------------------------------------------
            # Build request
            # --------------------------------------------------------

            request = ExtractionRequest(
                document_text=document_text,
                schema=schema,
                instructions=instructions,
                metadata=metadata,
            )

            prompt = ExtractionPrompt.build(
                document_text=request.document_text,
                schema=request.schema,
                instructions=request.instructions,
            )

            # --------------------------------------------------------
            # LLM
            # --------------------------------------------------------

            logger.info("Sending request to Gemini...")

            llm_response = await self.llm.generate_json(prompt)

            # --------------------------------------------------------
            # Parse response
            # --------------------------------------------------------

            if isinstance(llm_response, dict):
                extracted = llm_response
            else:
                extracted = ResponseParser.parse(llm_response)

            logger.info("Extraction completed successfully.")

            result = ExtractionResult(
                document_name=file_path.name,
                document_type=file_path.suffix.lower(),
                fields=extracted,
                metadata=metadata,
            )

            return ExtractionResponse(
                success=True,
                message="Extraction completed successfully.",
                result=result,
            )

        except Exception as exc:
            logger.exception(
                "Extraction failed for '%s'.",
                file_path.name,
            )

            return ExtractionResponse(
                success=False,
                message="Extraction failed.",
                errors=[str(exc)],
            )

    async def extract_text(
        self,
        file_path: str | Path,
    ) -> str:
        """
        Extract only raw text from a document.

        Args:
            file_path:
                Document path.

        Returns:
            Extracted text.
        """

        loader = LoaderFactory.get_loader(file_path)

        return await loader.load()

    async def health_check(self) -> bool:
        """
        Check whether the underlying LLM service is available.
        """

        return await self.llm.health_check()