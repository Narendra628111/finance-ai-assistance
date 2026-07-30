"""
Summarizer workflow node.

Invokes the SummarizerService and stores the
structured summary inside the workflow state.
"""

from __future__ import annotations

from backend.services.summarizer.summarizer import SummarizerService
from backend.utils.logger import get_logger
from backend.workflow.state import AssistantState
from backend.services.summarizer.summarizer import SummarizerService

logger = get_logger(__name__)


async def summarizer_node(
    state: AssistantState,
) -> AssistantState:
    """
    Summarize extracted document text.
    """

    logger.info("Executing Summarizer Node")

    service = SummarizerService()
    response = await service.summarize(
        state["extracted_text"],
    )

    state["summary"] = response.summary
    state["key_points"] = response.key_points
    state["document_type"] = response.document_type
    state["confidence"] = response.confidence

    logger.info("Summarizer Node completed")

    return state