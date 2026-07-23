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

    async def generate_from_image(
        self,
        image_bytes: bytes,
        prompt: str,
        mime_type: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate response from an image.
        """

        config = types.GenerateContentConfig(
            temperature=kwargs.get("temperature", self.temperature),
            max_output_tokens=kwargs.get(
                "max_output_tokens",
                self.max_output_tokens,
            ),
        )

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        )

        try:
            response = self.client.models.generate_content(
                model=kwargs.get("model", self.model),
                contents=[
                    image_part,
                    prompt,
                ],
                config=config,
            )

            if response.text is None:
                raise ValueError("Empty image response from Gemini.")

            return response.text.strip()

        except Exception:
            logger.exception("Gemini image generation failed.")
            raise
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """
        print("Embedding model:", settings.EMBEDDING_MODEL)
        
        try:
            response = self.client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=text,
            )

            return response.embeddings[0].values

        except Exception:
            logger.exception("Gemini embedding generation failed.")
            raise

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        BATCH_SIZE = 100
        all_embeddings = []

        for i in range(0, len(texts), BATCH_SIZE):
            batch = texts[i:i + BATCH_SIZE]

            response = self.client.models.embed_content(
                model=settings.EMBEDDING_MODEL,
                contents=batch,
            )

            batch_embeddings = [
                embedding.values
                for embedding in response.embeddings
            ]

            all_embeddings.extend(batch_embeddings)

            logger.info(
                "Embedded %d/%d chunks",
                min(i + len(batch), len(texts)),
                len(texts),
            )

        return all_embeddings

        
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