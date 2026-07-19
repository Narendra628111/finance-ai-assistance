"""
Classifier Agent.
"""

from __future__ import annotations

from backend.services.classifier.classifier import ClassifierService
from backend.services.classifier.schemas import ClassificationResponse


class ClassifierAgent:
    """
    Agent responsible for document classification.
    """

    def __init__(self) -> None:
        self._classifier = ClassifierService()

    async def classify(
        self,
        summary: str,
        entities: list[str],
    ) -> ClassificationResponse:
        """
        Classify extracted entities.

        Args:
            summary: Document summary.
            entities: Extracted entities.

        Returns:
            Structured classification response.
        """

        return await self._classifier.classify(
            summary=summary,
            entities=entities,
        )