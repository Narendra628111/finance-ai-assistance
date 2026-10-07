"""
RAG workflow node.

Connects the LangGraph workflow to the RAG service.
"""

from __future__ import annotations

from pathlib import Path

from backend.services.llm.llm_factory import LLMFactory
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.indexing_service import IndexingService
from backend.services.rag.rag_service import RAGService
from backend.services.rag.retrieval_service import RetrievalService
from backend.services.rag.vector_store import VectorStore
from backend.workflow.state import AssistantState
from backend.utils.logger import get_logger


logger = get_logger(__name__)


async def rag_node(
    state: AssistantState,
) -> AssistantState:
    """
    Execute the RAG pipeline.

    Uses:
        - Uploaded document text extracted by Docling
        - Summary when available
        - Qdrant knowledge base
        - Local embedding model
        - Configured LLM provider
    """

    logger.info("Executing RAG Node")

    # ---------------------------------------------------------
    # 1. Vector store
    # ---------------------------------------------------------

    vector_store = VectorStore()

    # ---------------------------------------------------------
    # 2. Embedding service
    # ---------------------------------------------------------

    embedding_service = EmbeddingService()

    # ---------------------------------------------------------
    # 3. Retrieval service
    # ---------------------------------------------------------

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    # ---------------------------------------------------------
    # 4. Indexing service
    # ---------------------------------------------------------

    indexing_service = IndexingService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    # ---------------------------------------------------------
    # 5. LLM
    # ---------------------------------------------------------

    llm = LLMFactory.create()

    # ---------------------------------------------------------
    # 6. RAG service
    # ---------------------------------------------------------

    rag_service = RAGService(
        indexing_service=indexing_service,
        retrieval_service=retrieval_service,
        llm=llm,
    )

    # ---------------------------------------------------------
    # 7. Uploaded document context
    # ---------------------------------------------------------

    document_text = state.get(
        "extracted_text",
        "",
    )

    summary = state.get(
        "summary",
        "",
    )

    file_path = state.get(
        "file_path",
    )

    # file_path comes from FastAPI as a string.
    # Convert it to Path before accessing .name.
    document_name = (
        Path(file_path).name
        if file_path
        else None
    )

    logger.info(
        "Document name: %s",
        document_name,
    )

    logger.info(
        "Extracted document text length: %d",
        len(document_text),
    )

    logger.info(
        "Summary length: %d",
        len(summary),
    )

    # ---------------------------------------------------------
    # 8. Ask RAG
    # ---------------------------------------------------------

    result = await rag_service.ask(
        question=state["user_query"],
        document_text=document_text,
        summary=summary,
        document_name=document_name,
    )

    # ---------------------------------------------------------
    # 9. Update workflow state
    # ---------------------------------------------------------

    state["rag_answer"] = result.get(
        "answer",
        "",
    )

    state["rag_sources"] = result.get(
        "sources",
        [],
    )

    state["final_answer"] = result.get(
        "answer",
        "",
    )

    logger.info(
        "RAG Node completed. Answer type: %s",
        result.get("answer_type"),
    )

    return state