"""
Summarizer Agent.
"""

from __future__ import annotations

from backend.services.summarizer.summarizer import SummarizerService
from backend.services.summarizer.schemas import SummaryResponse


class SummarizerAgent:
    """
    Agent responsible for document summarization.
    """

    def __init__(self) -> None:
        self._summarizer = SummarizerService()

    async def summarize(
        self,
        text: str,
    ) -> SummaryResponse:
        """
        Generate a structured summary for the given text.

        Args:
            text: Extracted document text.

        Returns:
            SummaryResponse containing the document summary.
        """

        return await self._summarizer.summarize(text)