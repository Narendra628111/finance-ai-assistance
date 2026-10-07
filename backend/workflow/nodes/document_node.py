"""
Document workflow node.

Loads and extracts text from uploaded documents.
"""

from __future__ import annotations

from backend.services.document.loader_factory import LoaderFactory
from backend.utils.logger import get_logger
from backend.workflow.state import AssistantState

logger = get_logger(__name__)


async def document_node(
    state: AssistantState,
) -> AssistantState:

    logger.info("Executing Document Node")

    loader = LoaderFactory.get_loader(
        state["file_path"],
    )

    text = await loader.load()

    state["extracted_text"] = text

    logger.info(
        "Extracted %d characters",
        len(text),
    )

    return state