"""
Google Gemini LLM service implementation.
"""

from __future__ import annotations

import json
from typing import Any

from google import genai
from google.genai import types

from backend.config import settings
from backend.services.llm.base_llm import BaseLLM
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GeminiService(BaseLLM):
    """
    Google Gemini service implementation.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL
        self.temperature = settings.GEMINI_TEMPERATURE
        self.max_output_tokens = settings.GEMINI_MAX_OUTPUT_TOKENS

    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a text response.
        """

        config = types.GenerateContentConfig(
            temperature=kwargs.get("temperature", self.temperature),
            max_output_tokens=kwargs.get(
                "max_output_tokens",
                self.max_output_tokens,
            ),
        )

        try:
            response = self.client.models.generate_content(
                model=kwargs.get("model", self.model),
                contents=prompt,
                config=config,
            )

            if response.text is None:
                raise ValueError("Empty response received from Gemini.")

            return response.text.strip()

        except Exception:
            logger.exception("Gemini text generation failed.")
            raise

    async def generate_json(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate structured JSON.
        """

        config = types.GenerateContentConfig(
            temperature=kwargs.get("temperature", self.temperature),
            response_mime_type="application/json",
            max_output_tokens=kwargs.get(
                "max_output_tokens",
                self.max_output_tokens,
            ),
        )

        try:
            response = self.client.models.generate_content(
                model=kwargs.get("model", self.model),
                contents=prompt,
                config=config,
            )

            if response.text is None:
                raise ValueError("Empty JSON response from Gemini.")

            return json.loads(response.text)

        except json.JSONDecodeError:
            logger.exception("Invalid JSON returned by Gemini.")
            raise

        except Exception:
            logger.exception("Gemini JSON generation failed.")
            raise

    

        
    async def health_check(self) -> bool:
        """
        Verify Gemini connectivity.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="Reply with OK.",
            )

            return (
                response.text is not None
                and response.text.strip() != ""
            )

        except Exception:
            logger.exception("Gemini health check failed.")
            return False