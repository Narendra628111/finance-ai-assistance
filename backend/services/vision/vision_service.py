"""
Vision Service.

Handles image analysis using Gemini Vision.
"""

from __future__ import annotations

from pathlib import Path

from backend.prompts.vision_prompt import VisionPrompt
from backend.services.llm.gemini_service import GeminiService
from backend.utils.logger import get_logger
from backend.utils.file_utils import FileUtils

logger = get_logger(__name__)


class VisionService:
    """
    Service responsible for image understanding.
    """

    def __init__(self) -> None:
        self.llm = GeminiService()

    async def analyze(
        self,
        image_path: str | Path,
        prompt: str,
    ) -> str:
        """
        Analyze an image using Gemini Vision.
        """

        image_path = Path(image_path)

        logger.info("Reading image: %s", image_path.name)

        image_bytes = image_path.read_bytes()

        mime_type = FileUtils.get_mime_type(image_path)

        logger.info("Sending image to Gemini Vision...")

        vision_prompt = VisionPrompt.build(prompt)

        response = await self.llm.generate_from_image(
            image_bytes=image_bytes,
            prompt=vision_prompt,
            mime_type=mime_type,
        )

        logger.info("Vision analysis completed.")

        return response