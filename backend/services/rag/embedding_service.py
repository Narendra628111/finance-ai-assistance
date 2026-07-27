"""
Embedding service.
"""

from backend.services.embeddings.base_embedding import BaseEmbedding


class EmbeddingService:

    def __init__(
        self,
        embedding_model: BaseEmbedding,
    ):
        self.embedding_model = embedding_model

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return await self.embedding_model.embed_text(text)

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return await self.embedding_model.embed_documents(texts)