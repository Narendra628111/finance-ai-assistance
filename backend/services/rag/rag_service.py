"""
RAG orchestration service.
"""

from __future__ import annotations

from backend.services.rag.retrieval_service import RetrievalService
from backend.services.llm.base_llm import BaseLLM
from backend.services.rag.indexing_service import IndexingService


class RAGService:
    """
    Orchestrates the Retrieval-Augmented Generation workflow.
    """

    def __init__(
        self,
        indexing_service: IndexingService,
        retrieval_service: RetrievalService,
        llm: BaseLLM,
    ) -> None:
        self.indexing_service = indexing_service
        self.retrieval_service = retrieval_service
        self.llm = llm

    async def build_index(
        self,
        rebuild: bool = False,
    ) -> int:
        """
        Build or rebuild the vector index.
        """

        return await self.indexing_service.build_index(
            rebuild=rebuild
        )

    async def ask(
        self,
        question: str,
    ) -> dict:
        """
        Answer a question using retrieved context.
        """

        documents = await self.retrieval_service.retrieve(
            question
        )

        if not documents:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded documents."
                ),
                "sources": [],
            }

        context = "\n\n".join(
            doc["content"]
            for doc in documents
        )

        prompt = f"""
You are a finance AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context,
respond with:

"I couldn't find that information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        answer = await self.llm.generate(prompt)

        return {
            "answer": answer,
            "sources": [
                {
                    "document": doc["source"],
                    "page": doc["page"],
                    "score": round(doc["score"], 4),
                }
                for doc in documents
            ],
        }