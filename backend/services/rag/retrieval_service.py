"""
Document retrieval service.
"""

from __future__ import annotations

from backend.config import settings
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.vector_store import VectorStore


class RetrievalService:
    """
    Retrieves similar documents from Qdrant.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:

        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def retrieve(
        self,
        question: str,
    ) -> list[dict]:

        embedding = await self.embedding_service.embed_text(
            question
        )

        results = self.vector_store.search(
            embedding=embedding,
            limit=settings.TOP_K_RESULTS,
        )
        return results
        