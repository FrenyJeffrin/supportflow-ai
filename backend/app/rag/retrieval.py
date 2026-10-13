from dataclasses import dataclass
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings

from app.models import (
    DocumentChunk,
    KnowledgeDocument,
)

from app.rag.embeddings import (
    embedding_service,
)

from app.observability.metrics import (
    RAG_LATENCY,
    RAG_SEARCHES,
)


@dataclass
class RetrievedChunk:
    content: str
    source: str
    title: str
    score: float


async def retrieve_context(
    db: AsyncSession,
    query: str,
    top_k: int | None = None,
) -> list[RetrievedChunk]:

    # Count every RAG retrieval attempt
    RAG_SEARCHES.inc()

    # Start measuring RAG latency
    start = time.perf_counter()

    try:
        if top_k is None:
            top_k = settings.rag_top_k

        # Generate query embedding
        query_embedding = await (
            embedding_service.embed_query(
                query
            )
        )

        # Calculate vector distance
        distance = (
            DocumentChunk.embedding
            .cosine_distance(
                query_embedding
            )
        )

        # Build vector search query
        statement = (
            select(
                DocumentChunk.content,
                KnowledgeDocument.source,
                KnowledgeDocument.title,
                distance.label(
                    "distance"
                ),
            )
            .join(
                KnowledgeDocument,
                KnowledgeDocument.id
                == DocumentChunk.document_id,
            )
            .order_by(distance)
            .limit(top_k)
        )

        # Execute vector search
        result = await db.execute(
            statement
        )

        rows = result.all()

        return [
            RetrievedChunk(
                content=row.content,
                source=row.source,
                title=row.title,
                score=max(0.0,1.0 - float(row.distance),),
                )
            for row in rows
        ]

    finally:
        # Record latency whether retrieval
        # succeeds OR fails
        RAG_LATENCY.observe(
            time.perf_counter()
            - start
        )