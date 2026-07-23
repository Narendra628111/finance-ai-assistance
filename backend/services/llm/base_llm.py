"""
Abstract base class for Large Language Model (LLM) providers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """
    Abstract interface for all LLM providers.

    Any LLM service (Gemini, OpenAI, Claude, Ollama, etc.)
    should inherit from this class.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a text response from the LLM.

        Args:
            prompt: Input prompt.
            **kwargs: Provider-specific parameters.

        Returns:
            Generated text response.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Generate a structured JSON response.

        Args:
            prompt: Input prompt.
            **kwargs: Provider-specific parameters.

        Returns:
            Parsed JSON response.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_from_image(
        self,
        image_bytes: bytes,
        prompt: str,
        mime_type: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response using an image and prompt.

        Args:
            image_bytes: Image content as bytes.
            prompt: User prompt.
            mime_type: Image MIME type.
            **kwargs: Provider-specific parameters.

        Returns:
            Generated text response.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding vector for a text.

        Args:
            text: Input text.

        Returns:
            Embedding vector.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify whether the provider is reachable.

        Returns:
            True if healthy, otherwise False.
        """
        raise NotImplementedError