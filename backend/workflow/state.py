from __future__ import annotations

from pathlib import Path
from typing import Any

from typing_extensions import TypedDict

from backend.services.classifier.schemas import ClassificationResponse


class AssistantState(TypedDict, total=False):

    # Input
    input_type: str
    user_query: str
    file_path: Path |None

    # Processing
    extracted_text: str
    vision_result: str

    summary: str
    key_points: list[str]

    # Classification
    classification: str
    classification_confidence: float

    # RAG
    rag_answer: str
    rag_sources: list[dict]

    # Final
    final_answer: str