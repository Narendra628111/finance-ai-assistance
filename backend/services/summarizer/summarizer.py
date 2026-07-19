from pydantic import ValidationError

from backend.services.llm.base_llm import BaseLLM
from backend.services.llm.llm_factory import LLMFactory

from .base import BaseSummarizer
from .exceptions import InvalidSummaryError, SummarizationError
from .prompt import build_summary_prompt
from .schemas import SummaryResponse


class SummarizerService(BaseSummarizer):
    """
    Gemini implementation of the Summarizer Agent.
    """

    def __init__(
        self,
        llm: BaseLLM | None = None,
    ):
        self._llm = llm or LLMFactory.create()

    async def summarize(
        self,
        text: str,
    ) -> SummaryResponse:

        if not text or not text.strip():
            raise SummarizationError(
                "Input text cannot be empty."
            )

        prompt = build_summary_prompt(text)

        try:
            data = await self._llm.generate_json(
                prompt=prompt,
                temperature=0.2,
            )

        except Exception as exc:
            raise SummarizationError(
                "Failed to summarize document."
            ) from exc

        try:
            return SummaryResponse.model_validate(data)

        except ValidationError as exc:
            raise InvalidSummaryError(
                "Invalid summary response."
            ) from exc