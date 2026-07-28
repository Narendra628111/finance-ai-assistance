"""
RAG orchestration service.
"""

from __future__ import annotations

from backend.prompts.domain_prompt import DOMAIN_PROMPT
from backend.prompts.general_prompt import GENERAL_PROMPT
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
        return await self.indexing_service.build_index(
            rebuild=rebuild
        )

    async def ask(
        self,
        question: str,
    ) -> dict:

        # ---------------------------------------------
        # Step 1 : Finance domain check
        # ---------------------------------------------

        if not await self.is_finance_question(question):
            return {
                "answer": (
                    "This assistant is designed to answer "
                    "banking and finance related questions only."
                ),
                "answer_type": "not_found",
                "sources": [],
            }

        # ---------------------------------------------
        # Step 2 : Retrieve documents
        # ---------------------------------------------

        documents = await self.retrieval_service.retrieve(
            question
        )

        if not documents:
            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded documents."
                ),
                "answer_type": "not_found",
                "sources": [],
            }

        # ---------------------------------------------
        # Step 3 : Build context
        # ---------------------------------------------

        context = "\n\n".join(
            doc["content"]
            for doc in documents
        )

        prompt = RAG_PROMPT.format(
            context=context,
            question=question,
        )

        print("=" * 80)
        print("QUESTION")
        print(question)
        print("=" * 80)

        print("=" * 80)
        print("RETRIEVED CONTEXT")
        print(context)
        print("=" * 80)

        answer = await self.llm.generate(prompt)

        print("=" * 80)
        print("GROUNDED ANSWER")
        print(answer)
        print("=" * 80)

        # ---------------------------------------------
        # Step 4 : Detect if context is insufficient
        # ---------------------------------------------

        failure_phrases = [
            "i couldn't find that information",
            "not found in the provided documents",
            "not available in the provided documents",
        ]

        if any(
            phrase in answer.lower()
            for phrase in failure_phrases
        ):

            general_prompt = GENERAL_PROMPT.format(
                question=question,
            )

            general_answer = await self.llm.generate(
                general_prompt
            )

            return {
                "answer": general_answer,
                "answer_type": "general",
                "sources": [],
            }

        # ---------------------------------------------
        # Step 5 : Remove duplicate sources
        # ---------------------------------------------

        unique_sources = []
        seen = set()

        for doc in documents:

            key = (
                doc["source"],
                doc["page"],
            )

            if key in seen:
                continue

            seen.add(key)

            unique_sources.append(
                {
                    "document": doc["source"],
                    "page": doc["page"],
                    "score": round(
                        doc["score"],
                        4,
                    ),
                }
            )

        return {
            "answer": answer,
            "answer_type": "grounded",
            "sources": unique_sources,
        }

    async def is_finance_question(
        self,
        question: str,
    ) -> bool:
        """
        Determine whether the question belongs
        to the finance domain.
        """

        prompt = DOMAIN_PROMPT.format(
            question=question,
        )

        response = await self.llm.generate(
            prompt
        )

        return response.strip().lower() == "finance"