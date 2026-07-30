from abc import ABC, abstractmethod

from .schemas import ClassificationResponse


class BaseClassifier(ABC):
    """
    Abstract base class for all classifier implementations.
    """

    @abstractmethod
    async def classify(
        self,
        text: str,
    ) -> ClassificationResponse:
        """
        Classify the given text.

        Args:
            text: Input text to classify.

        Returns:
            ClassificationResponse
        """
        raise NotImplementedError