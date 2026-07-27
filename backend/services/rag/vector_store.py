"""
Qdrant vector store service.
"""

from __future__ import annotations

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VectorStore:
    """
    Handles all Qdrant operations.
    """

    def __init__(self) -> None:
        self.client = QdrantClient(
            path=str(settings.QDRANT_PATH)
        )

        self.collection = settings.QDRANT_COLLECTION_NAME

        self._create_collection()

    def _create_collection(self) -> None:
        """
        Create collection if it does not exist.
        """

        collections = self.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        if self.collection in names:
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=settings.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            "Created Qdrant collection '%s'.",
            self.collection,
        )

    def upsert(
        self,
        points: list[PointStruct],
    ) -> None:
        """
        Store vectors.
        """

        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )

    def search(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        """
        Search similar vectors.
        """

        response = self.client.query_points(
            collection_name=self.collection,
            query=embedding,
            limit=limit,
            with_payload=True,
        )


    

        documents = []

        for point in response.points:
            documents.append(
                {
                    "content": point.payload["content"],
                    "source": point.payload["source"],
                    "page": point.payload["page"],
                    "score": point.score,
                }
            )

        return documents

    
    
    def recreate_collection(self) -> None:
        """
        Recreate the collection to avoid duplicate vectors.
        """

        if self.client.collection_exists(self.collection):
            self.client.delete_collection(
                collection_name=self.collection
            )

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=settings.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            "Recreated collection '%s'.",
            self.collection,
        )
    