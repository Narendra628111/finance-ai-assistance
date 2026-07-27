from abc import ABC, abstractmethod


class BaseEmbedding(ABC):

    @abstractmethod
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        pass

    @abstractmethod
    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        pass