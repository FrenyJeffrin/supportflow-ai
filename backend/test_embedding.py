import asyncio

from app.rag.embeddings import (
    embedding_service,
)


async def main():

    vector = await (embedding_service.embed_query(
            "Can I return my order?"
        ))

    print(
        "Dimensions:",
        len(vector),
    )

    print(
        "First 5 values:",
        vector[:5],
    )


asyncio.run(main())