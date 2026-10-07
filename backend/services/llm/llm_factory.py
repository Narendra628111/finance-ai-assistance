from backend.config import settings
from backend.services.llm.base_llm import BaseLLM
from backend.services.llm.gemini_service import GeminiService
from backend.services.llm.groq_service import GroqService


class LLMFactory:

    @staticmethod
    def create() -> BaseLLM:

        provider = settings.LLM_PROVIDER.lower()

        if provider == "groq":
            return GroqService()

        if provider == "gemini":
            return GeminiService()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )