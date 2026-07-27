from backend.services.embeddings.minilm_embedding import MiniLMEmbedding


class EmbeddingFactory:

    @staticmethod
    def create():
        return MiniLMEmbedding()