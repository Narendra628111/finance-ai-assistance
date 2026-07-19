"""
Factory for creating LLM service instances.
"""

from __future__ import annotations

from backend.config import settings
from backend.core.exception import ConfigurationError
from backend.services.llm.base_llm import BaseLLM
from backend.services.llm.gemini_service import GeminiService


class LLMFactory:
    """Factory class for creating LLM service instances."""

    _providers: dict[str, type[BaseLLM]] = {
        "gemini": GeminiService,
    }

    @classmethod
    def register(
        cls,
        name: str,
        provider: type[BaseLLM],
    ) -> None:
        """
        Register a new LLM provider.
        """
        cls._providers[name.lower()] = provider

    @classmethod
    def create(
        cls,
        provider: str | None = None,
    ) -> BaseLLM:
        """
        Create an LLM service instance.

        Args:
            provider: Optional provider name.
                      If omitted, the value from settings is used.

        Returns:
            BaseLLM implementation.
        """

        provider_name = (
            provider or settings.LLM_PROVIDER
        ).lower()

        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())

            raise ConfigurationError(
                f"Unsupported LLM provider '{provider_name}'. "
                f"Available providers: {available}"
            )

        return cls._providers[provider_name]()