"""
Text splitting service for RAG.

Splits LangChain documents into smaller overlapping chunks.
"""

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.config import settings


class TextSplitterService:
    """
    Splits documents into chunks suitable for vector embeddings.
    """

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split documents into overlapping chunks.

        Args:
            documents: List of LangChain documents.

        Returns:
            List of chunked documents.
        """
        return self.splitter.split_documents(documents)