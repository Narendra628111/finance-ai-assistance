"""
Vision Agent.
"""

from __future__ import annotations

from pathlib import Path

from backend.models.vision_models import VisionResponse
from backend.services.vision.vision_service import VisionService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VisionAgent:
    """
    Agent responsible for image analysis.
    """

    def __init__(self) -> None:
        self._vision = VisionService()

    async def analyze(
        self,
        image_path: str | Path,
        prompt: str | None = None,
    ) -> VisionResponse:

        if not prompt:
            prompt = "Describe this image in detail."

        try:
            analysis = await self._vision.analyze(
                image_path=image_path,
                prompt=prompt,
            )

            return VisionResponse(
                success=True,
                message="Image analyzed successfully.",
                analysis=analysis,
            )

        except Exception as exc:
            logger.exception("Vision analysis failed.")

            return VisionResponse(
                success=False,
                message="Image analysis failed.",
                analysis="",
                errors=[str(exc)],
            )
        

    async def health_check(self) -> bool:
        """
        Check whether the Vision service is available.
        """

        return await self._vision.llm.health_check()