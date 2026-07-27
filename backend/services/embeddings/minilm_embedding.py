from sentence_transformers import SentenceTransformer

from backend.services.embeddings.base_embedding import BaseEmbedding


class MiniLMEmbedding(BaseEmbedding):

    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            batch_size=64,
            show_progress_bar=True,
            convert_to_numpy=True,
        )

        return embeddings.tolist()