from backend.services.llm.llm_factory import LLMFactory
from backend.services.rag.embedding_service import EmbeddingService
from backend.services.rag.vector_store import VectorStore
from backend.services.rag.indexing_service import IndexingService
from backend.services.rag.retrieval_service import RetrievalService
from backend.services.rag.rag_service import RAGService
from backend.agents.rag_agent import RAGAgent
from backend.services.embeddings.embedding_factory import EmbeddingFactory

def get_rag_agent() -> RAGAgent:

    llm = LLMFactory.create()

    embedding_model = EmbeddingFactory.create()

    embedding = EmbeddingService(embedding_model)

    vector_store = VectorStore()

    indexing = IndexingService(
        embedding,
        vector_store,
    )

    retrieval = RetrievalService(
        embedding,
        vector_store,
    )

    rag_service = RAGService(
        indexing,
        retrieval,
        llm,
    )

    return RAGAgent(rag_service)