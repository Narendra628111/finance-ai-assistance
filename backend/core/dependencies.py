"""
Application dependency providers.
"""

from __future__ import annotations

from backend.agents.rag_agent import RAGAgent
from backend.agents.workflow_agent import WorkflowAgent

from backend.services.embeddings.embedding_factory import (
    EmbeddingFactory,
)
from backend.services.llm.llm_factory import (
    LLMFactory,
)
from backend.services.rag.embedding_service import (
    EmbeddingService,
)
from backend.services.rag.indexing_service import (
    IndexingService,
)
from backend.services.rag.rag_service import (
    RAGService,
)
from backend.services.rag.retrieval_service import (
    RetrievalService,
)
from backend.services.rag.vector_store import (
    VectorStore,
)

from backend.services.rag.rag_factory import (
    RAGFactory,
)


def get_rag_service():

    return RAGFactory.create()
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