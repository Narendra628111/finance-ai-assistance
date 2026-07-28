"""
Cross-encoder reranker service.
"""

from sentence_transformers import CrossEncoder


class RerankerService:
    """
    Re-ranks retrieved chunks using a CrossEncoder.
    """

    def __init__(self) -> None:
        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:

        if not documents:
            return []

        pairs = [
            (query, doc["content"])
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        documents.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )

        return documents[:top_k]