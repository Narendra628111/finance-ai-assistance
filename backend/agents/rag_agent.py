"""
RAG Agent.
"""

from backend.services.rag.rag_service import RAGService


class RAGAgent:
    """
    Agent responsible for interacting with the RAG service.
    """

    def __init__(
        self,
        rag_service: RAGService,
    ) -> None:
        self.rag_service = rag_service

    async def build_index(
        self,
        rebuild: bool = False,
    ) -> int:
        """
        Build or rebuild the vector index.
        """
        return await self.rag_service.build_index(
            rebuild=rebuild
        )

    async def ask(
        self,
        question: str,
    ) -> dict:
        """
        Ask a question to the RAG system.
        """
        return await self.rag_service.ask(question)