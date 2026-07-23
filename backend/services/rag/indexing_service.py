"""
Document indexing service.
"""

from __future__ import annotations

import uuid

from qdrant_client.models import PointStruct

from backend.services.rag.document_loader import DocumentLoader
from backend.services.rag.text_splitter import TextSplitterService
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.vector_store import VectorStore
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class IndexingService:
    """
    Handles loading, splitting, embedding, and indexing documents.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self.loader = DocumentLoader()
        self.splitter = TextSplitterService()
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def build_index(
        self,
        rebuild: bool = False,
    ) -> int:
        """
        Build or rebuild the vector index.

        Args:
            rebuild: If True, clears the existing collection
                     before indexing.

        Returns:
            Number of indexed chunks.
        """

        if rebuild:
            self.vector_store.recreate_collection()

        documents = self.loader.load_documents()

        if not documents:
            logger.warning("No PDF documents found.")
            return 0

        chunks = self.splitter.split_documents(documents)

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = await self.embedding_service.embed_documents(
            texts
        )

        points: list[PointStruct] = []

        for chunk, embedding in zip(chunks, embeddings):

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "content": chunk.page_content,
                        "source": chunk.metadata.get("source", ""),
                        "page": chunk.metadata.get("page", 0),
                    },
                )
            )

        self.vector_store.upsert(points)

        logger.info(
            "Successfully indexed %d chunks.",
            len(points),
        )
        print("Documents:", len(documents))
        print("Chunks:", len(chunks))
        print("Embeddings:", len(embeddings))
        return len(points)
        