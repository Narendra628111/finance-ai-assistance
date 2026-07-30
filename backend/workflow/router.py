"""
Workflow routing functions.
"""

from __future__ import annotations

from backend.workflow.state import AssistantState


def route_input(
    state: AssistantState,
) -> str:
    """
    Route the workflow based on input type.
    """

    input_type = (
        state.get("input_type", "")
        .strip()
        .lower()
    )

    if input_type == "image":
        return "vision"

    if input_type in {
        "pdf",
        "docx",
        "txt",
    }:
        return "document"

    return "text"


def route_after_classifier(
    state: AssistantState,
) -> str:
    """
    Route after classification.
    """

    return "rag"