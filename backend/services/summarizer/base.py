from abc import ABC, abstractmethod

from .schemas import SummaryResponse


class BaseSummarizer(ABC):
    """
    Abstract base class for all summarizer implementations.
    """

    @abstractmethod
    async def summarize(self, text: str) -> SummaryResponse:
        """
        Generate a structured summary for the provided text.

        Args:
            text: Extracted document text.

        Returns:
            SummaryResponse containing the summary,
            key points, document type, and confidence score.
        """
        raise NotImplementedError