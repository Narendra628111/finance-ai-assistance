"""
Workflow routing functions.
"""

from __future__ import annotations

from backend.workflow.state import AssistantState


def route_input(state: AssistantState) -> str:
    """
    Route text separately from uploaded documents.
    """

    input_type = str(
        state.get("input_type") or "text"
    ).strip().lower()

    if input_type in {
        "pdf",
        "docx",
        "txt",
        "image",
        "png",
        "jpg",
        "jpeg",
        "webp",
        "bmp",
        "tif",
        "tiff",
    }:
        return "document"

    return "text"

def route_after_classifier(state: AssistantState) -> str:
    """
    Route classified requests to the RAG node.

    For the current MVP, every request that reaches
    the classifier is grounded using the knowledge base.
    """

    return "rag"