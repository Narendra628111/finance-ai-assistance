"""
Embedding service.
"""

from backend.services.llm.base_llm import BaseLLM


class EmbeddingService:

    def __init__(
        self,
        llm: BaseLLM,
    ) -> None:
        self.llm = llm

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return await self.llm.embed_text(text)

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self.llm.embed_documents(texts)