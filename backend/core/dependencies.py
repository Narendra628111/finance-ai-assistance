"""
Application dependency providers.
"""

from __future__ import annotations

from backend.agents.rag_agent import RAGAgent
from backend.agents.workflow_agent import WorkflowAgent

from backend.services.llm.llm_factory import LLMFactory
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.indexing_service import IndexingService
from backend.services.rag.rag_service import RAGService
from backend.services.rag.retrieval_service import RetrievalService
from backend.services.rag.vector_store import VectorStore


def get_rag_service() -> RAGService:
    """
    Create and return a RAG service.
    """

    vector_store = VectorStore()

    embedding_service = EmbeddingService()

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    indexing_service = IndexingService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    llm = LLMFactory.create()

    return RAGService(
        indexing_service=indexing_service,
        retrieval_service=retrieval_service,
        llm=llm,
    )


def get_rag_agent() -> RAGAgent:
    """
    Dependency provider for RAGAgent.
    """

    return RAGAgent(
        get_rag_service(),
    )


def get_workflow_agent() -> WorkflowAgent:
    """
    Dependency provider for WorkflowAgent.
    """

    return WorkflowAgent()