"""
Vision workflow node.

Invokes the VisionService and stores the analysis
inside the workflow state.
"""

from __future__ import annotations

from backend.services.vision.vision_service import VisionService
from backend.workflow.state import AssistantState
from backend.utils.logger import get_logger
from backend.services.vision.vision_service import VisionService

logger = get_logger(__name__)


async def vision_node(
    state: AssistantState,
) -> AssistantState:
    """
    Analyze an uploaded image.
    """

    logger.info("Executing Vision Node")

    service = VisionService()

    result = await service.analyze(
        image_path=state["file_path"],
        prompt=state["user_query"],
    )

    state["vision_result"] = result

    logger.info("Vision Node completed")

    return state