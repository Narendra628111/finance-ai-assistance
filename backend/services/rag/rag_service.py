"""
RAG orchestration service.
"""

from __future__ import annotations

from backend.prompts.general_prompt import GENERAL_PROMPT
from backend.prompts.rag_prompt import RAG_PROMPT
from backend.services.llm.base_llm import BaseLLM
from backend.services.rag.indexing_service import IndexingService
from backend.services.rag.retrieval_service import RetrievalService


class RAGService:
    """
    Orchestrates the Retrieval-Augmented Generation workflow.

    Supports:
    - Normal text questions
    - Uploaded documents
    - Uploaded images
    - OCR extracted text
    - Knowledge-base retrieval
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
        Build or rebuild the knowledge-base index.
        """

        return await self.indexing_service.build_index(
            rebuild=rebuild,
        )

    async def ask(
        self,
        question: str,
        document_text: str = "",
        summary: str = "",
        key_points: list[str] | None = None,
        document_name: str | None = None,
    ) -> dict:
        """
        Answer a question using:

        1. Uploaded document/image information
        2. OCR extracted text
        3. Document summary
        4. Knowledge-base retrieval
        5. LLM generation
        """

        key_points = key_points or []

        # =====================================================
        # 1. Retrieve knowledge-base context
        # =====================================================

        documents = await self.retrieval_service.retrieve(
            question,
        )

        # =====================================================
        # 2. Build retrieved knowledge
        # =====================================================

        knowledge_context = ""

        if documents:

            knowledge_context = "\n\n".join(
                doc["content"]
                for doc in documents
            )

        # =====================================================
        # 3. Build uploaded document context
        # =====================================================

        uploaded_context = ""

        if document_text.strip():

            uploaded_context += (
                "\nUPLOADED DOCUMENT / IMAGE TEXT:\n"
            )

            uploaded_context += document_text.strip()

        if summary.strip():

            uploaded_context += (
                "\n\nDOCUMENT SUMMARY:\n"
            )

            uploaded_context += summary.strip()

        if key_points:

            uploaded_context += (
                "\n\nKEY POINTS:\n"
            )

            uploaded_context += "\n".join(
                f"- {point}"
                for point in key_points
            )

        # =====================================================
        # 4. Debug information
        # =====================================================

        print("=" * 80)
        print("RAG QUESTION")
        print(question)
        print("=" * 80)

        print("UPLOADED DOCUMENT CONTEXT")
        print(uploaded_context[:5000])
        print("=" * 80)

        print("RETRIEVED KNOWLEDGE")

        for doc in documents:

            print(
                f"Score: {doc['score']:.4f} | "
                f"Source: {doc['source']} | "
                f"Page: {doc['page']}"
            )

        print("=" * 80)

        # =====================================================
        # 5. No information at all
        # =====================================================

        if not uploaded_context.strip() and not knowledge_context.strip():

            return {
                "answer": (
                    "I couldn't find enough information "
                    "to answer this question."
                ),
                "answer_type": "not_found",
                "sources": [],
            }

        # =====================================================
        # 6. Build RAG prompt
        # =====================================================

        prompt = RAG_PROMPT.format(
            question=question,
            context=knowledge_context,
            uploaded_context=uploaded_context,
        )

        # =====================================================
        # 7. Generate answer
        # =====================================================

        answer = await self.llm.generate(
            prompt,
        )

        print("=" * 80)
        print("GROUNDED ANSWER")
        print(answer)
        print("=" * 80)

        # =====================================================
        # 8. Detect insufficient answer
        # =====================================================

        failure_phrases = {
            "i couldn't find that information",
            "not found in the provided documents",
            "not available in the provided documents",
            "i don't have enough information",
            "insufficient information",
            "there is no uploaded document",
            "no uploaded document or image",
        }

        if any(
            phrase in answer.lower()
            for phrase in failure_phrases
        ):

            # If we have uploaded image/document text,
            # don't throw it away and ask the general LLM.
            if uploaded_context.strip():

                general_prompt = f"""
You are a banking and finance assistant.

The user uploaded a document or image.

Use the extracted information below to answer
the user's question.

USER QUESTION:
{question}

UPLOADED DOCUMENT / IMAGE INFORMATION:
{uploaded_context}

KNOWLEDGE BASE INFORMATION:
{knowledge_context}

Instructions:
- Explain what is actually visible in the uploaded document/image.
- Use the extracted OCR text as the source of truth.
- Use the knowledge base only when it helps explain
  the financial meaning.
- Do not claim that no image or document was provided.
- Do not invent values that are not present.
"""

                answer = await self.llm.generate(
                    general_prompt,
                )

                return {
                    "answer": answer,
                    "answer_type": "document",
                    "sources": self._build_sources(
                        documents,
                    ),
                }

            # No uploaded document, so use general answer.

            general_prompt = GENERAL_PROMPT.format(
                question=question,
            )

            general_answer = await self.llm.generate(
                general_prompt,
            )

            return {
                "answer": general_answer,
                "answer_type": "general",
                "sources": [],
            }

        # =====================================================
        # 9. Build source list
        # =====================================================

        unique_sources = self._build_sources(
            documents,
        )

        # =====================================================
        # 10. Return final result
        # =====================================================

        answer_type = (
            "document"
            if uploaded_context.strip()
            else "grounded"
        )

        return {
            "answer": answer,
            "answer_type": answer_type,
            "sources": unique_sources,
        }

    @staticmethod
    def _build_sources(
        documents: list[dict],
    ) -> list[dict]:
        """
        Remove duplicate sources.
        """

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

        return unique_sources