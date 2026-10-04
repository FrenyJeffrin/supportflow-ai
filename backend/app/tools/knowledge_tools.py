import json

from langchain_core.tools import tool

from app.database import AsyncSessionLocal

from app.rag.retrieval import (
    retrieve_context,
)


@tool
async def search_knowledge_base(
    query: str,
) -> str:
    """
    Search SupportFlow company policies.

    Use this tool for questions about refunds,
    returns, shipping, warranty, or customer
    support policies.
    """

    async with AsyncSessionLocal() as db:

        results = await retrieve_context(
            db=db,
            query=query,
        )

        payload = [
            {
                "title": item.title,
                "source": item.source,
                "score": round(
                    item.score,
                    3,
                ),
                "content": item.content,
            }
            for item in results
        ]

        return json.dumps(payload)