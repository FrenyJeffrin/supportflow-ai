import asyncio

from app.database import AsyncSessionLocal

from app.rag.retrieval import (
    retrieve_context,
)


async def main():

    async with (
        AsyncSessionLocal()
        as db
    ):

        results = await (
            retrieve_context(
                db,
                (
                    "My delivery is more "
                    "than seven days late. "
                    "Can I get my money back?"
                ),
            )
        )


        for index, item in enumerate(
            results,
            start=1,
        ):

            print(
                f"\nRESULT {index}"
            )

            print(
                f"Source: {item.source}"
            )

            print(
                f"Score: {item.score:.3f}"
            )

            print(
                item.content
            )


asyncio.run(main())