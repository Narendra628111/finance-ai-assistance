"""
RAG workflow node.

Retrieves grounded answers from the banking knowledge base.
"""

from __future__ import annotations

from backend.services.rag.rag_factory import RAGFactory
from backend.utils.logger import get_logger
from backend.workflow.state import AssistantState

logger = get_logger(__name__)


async def rag_node(
    state: AssistantState,
) -> AssistantState:
    """
    Execute the RAG workflow.
    """

    logger.info("Executing RAG Node")

    rag_service = RAGFactory.create()

    result = await rag_service.ask(
        question=state["user_query"],
    )

    state["rag_answer"] = result["answer"]
    state["rag_sources"] = result["sources"]
    state["final_answer"] = result["answer"]

    logger.info("RAG Node completed")

    return state