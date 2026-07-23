from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from backend.config import settings


class DocumentLoader:
    """
    Loads all PDF documents from the configured policies directory.
    """

    def __init__(self):
        self.policies_dir = settings.POLICIES_DIR

    def load_documents(self) -> List[Document]:
        documents = []

        if not self.policies_dir.exists():
            return documents

        for pdf in self.policies_dir.rglob("*.pdf"):
            print(f"Loading: {pdf}")

            loader = PyPDFLoader(str(pdf))
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = pdf.relative_to(self.policies_dir).as_posix()

            documents.extend(docs)

        print(f"Loaded {len(documents)} pages")

        return documents