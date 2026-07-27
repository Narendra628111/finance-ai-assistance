"""
RAG orchestration service.
"""

from __future__ import annotations

from backend.prompts.rag_prompt import RAG_PROMPT
from backend.services.llm.base_llm import BaseLLM
from backend.services.rag.indexing_service import IndexingService
from backend.services.rag.retrieval_service import RetrievalService


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

        prompt = RAG_PROMPT.format(
            context=context,
            question=question,
        )

        answer = await self.llm.generate(prompt)

        # Remove duplicate source entries
        unique_sources = []
        seen = set()

        for doc in documents:
            key = (
                doc["source"],
                doc["page"],
            )

            if key not in seen:
                seen.add(key)

                unique_sources.append(
                    {
                        "document": doc["source"],
                        "page": doc["page"],
                        "score": round(doc["score"], 4),
                    }
                )

        return {
            "answer": answer,
            "sources": unique_sources,
        }