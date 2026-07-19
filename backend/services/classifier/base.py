from abc import ABC, abstractmethod

from .schemas import ClassificationResponse


class BaseClassifier(ABC):
    """
    Abstract base class for all classifier implementations.
    """

    @abstractmethod
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
            ClassificationResponse
        """
        raise NotImplementedError