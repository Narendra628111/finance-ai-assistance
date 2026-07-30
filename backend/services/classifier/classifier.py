from pydantic import ValidationError

from backend.services.llm.base_llm import BaseLLM
from backend.services.llm.llm_factory import LLMFactory

from .base import BaseClassifier
from .exceptions import (
    ClassificationError,
    InvalidClassificationError,
)
from .prompt import build_classifier_prompt
from .schemas import ClassificationResponse


class ClassifierService(BaseClassifier):
    """
    Gemini implementation of the Classifier Agent.
    """

    def __init__(
        self,
        llm: BaseLLM | None = None,
    ) -> None:
        self._llm = llm or LLMFactory.create()

    async def classify(
        self,
        text: str,
    ) -> ClassificationResponse:
        """
        Classify the given text.
        """

        if not text.strip():
            raise ClassificationError(
                "Input text cannot be empty."
            )

        prompt = build_classifier_prompt(
            text=text,
        )

        try:
            data = await self._llm.generate_json(
                prompt=prompt,
                temperature=0.0,
            )

        except Exception as exc:
            raise ClassificationError(
                "Failed to classify document."
            ) from exc

        try:
            return ClassificationResponse.model_validate(
                data,
            )

        except ValidationError as exc:
            raise InvalidClassificationError(
                "Invalid classification response."
            ) from exc