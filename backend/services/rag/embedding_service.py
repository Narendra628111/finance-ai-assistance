"""
Local embedding service.

Uses all-MiniLM-L6-v2 to generate 384-dimensional
embeddings locally.
"""

from __future__ import annotations

import asyncio

from sentence_transformers import SentenceTransformer

from backend.config import settings
from backend.utils.logger import get_logger


logger = get_logger(__name__)


class EmbeddingService:
    """
    Generates local embeddings using Sentence Transformers.
    """

    def __init__(self) -> None:
        logger.info(
            "Loading embedding model: %s",
            settings.EMBEDDING_MODEL,
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL,
        )

        logger.info(
            "Embedding model loaded successfully.",
        )

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty."
            )

        embedding = await asyncio.to_thread(
            self.model.encode,
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """

        if not texts:
            return []

        embeddings = await asyncio.to_thread(
            self.model.encode,
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()