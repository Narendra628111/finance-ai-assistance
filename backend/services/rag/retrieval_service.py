"""
Document retrieval service.
"""

from __future__ import annotations

from backend.config import settings
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.vector_store import VectorStore
from backend.services.reranker.reranker_service import (
    RerankerService,
)


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
        self.reranker = RerankerService()

    async def retrieve(
        self,
        question: str,
        ) -> list[dict]:

        embedding = await self.embedding_service.embed_text(
            question
        )

        # Retrieve candidates from Qdrant
        documents = self.vector_store.search(
            embedding=embedding,
            limit=10,
        )

        # ---------------------------------------
        # Remove duplicate chunks
        # ---------------------------------------

        unique_docs = []
        seen = set()

        for doc in documents:

            content = doc["content"].strip()

            if content in seen:
                continue

            seen.add(content)
            unique_docs.append(doc)

        # ---------------------------------------
        # Rerank
        # ---------------------------------------

        reranked = self.reranker.rerank(
            query=question,
            documents=unique_docs,
            top_k=5,
        )

        print("=" * 80)
        print("AFTER RERANKING")

        for doc in reranked:
            print(
                f"CrossEncoder: {doc['rerank_score']:.4f}"
            )
            print(
                f"Vector Score: {doc['score']:.4f}"
            )
            print(
                f"Source: {doc['source']}"
            )
            print("-" * 60)

        print("=" * 80)

        return reranked