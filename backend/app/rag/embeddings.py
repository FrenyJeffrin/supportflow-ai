from langchain_ollama import OllamaEmbeddings

from app.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
            dimensions=settings.embedding_dimensions,
        )

    async def embed_query(
        self,
        text: str,
    ) -> list[float]:

        return await self.embeddings.aembed_query(
            text
        )

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        return await self.embeddings.aembed_documents(
            texts
        )


embedding_service = EmbeddingService()