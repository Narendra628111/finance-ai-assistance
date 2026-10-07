"""
Groq LLM implementation.
"""

from __future__ import annotations

import json
from typing import Any

from groq import AsyncGroq

from backend.config import settings
from backend.services.llm.base_llm import BaseLLM
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GroqService(BaseLLM):
    """
    Groq implementation of BaseLLM.
    """

    def __init__(self) -> None:
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        self.max_tokens = settings.GROQ_MAX_OUTPUT_TOKENS

    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a text response.
        """

        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get(
                    "model",
                    self.model,
                ),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant for banking and finance."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=kwargs.get(
                    "temperature",
                    self.temperature,
                ),
                max_tokens=kwargs.get(
                    "max_tokens",
                    self.max_tokens,
                ),
            )

            content = response.choices[0].message.content

            if content is None:
                raise ValueError(
                    "Groq returned an empty response."
                )

            return content.strip()

        except Exception:
            logger.exception(
                "Groq text generation failed."
            )
            raise

    async def generate_json(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate structured JSON.
        """

        try:
            response = await self.client.chat.completions.create(
                model=kwargs.get(
                    "model",
                    self.model,
                ),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a JSON API.\n"
                            "Always return ONLY valid JSON.\n"
                            "Never use markdown.\n"
                            "Never explain.\n"
                            "Never wrap JSON inside code blocks."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={
                    "type": "json_object",
                },
                temperature=0,
                max_tokens=kwargs.get(
                    "max_tokens",
                    self.max_tokens,
                ),
            )

            content = response.choices[0].message.content

            if content is None:
                raise ValueError(
                    "Groq returned an empty JSON response."
                )

            return json.loads(content)

        except json.JSONDecodeError:
            logger.exception(
                "Groq returned invalid JSON."
            )
            raise

        except Exception:
            logger.exception(
                "Groq JSON generation failed."
            )
            raise

    async def health_check(self) -> bool:
        """
        Verify Groq connectivity.
        """

        try:
            response = await self.generate(
                "Reply with only OK."
            )

            return response.strip().upper() == "OK"

        except Exception:
            logger.exception(
                "Groq health check failed."
            )
            return False