import asyncio

from langchain_ollama import OllamaEmbeddings


TEXT = """# SupportFlow Refund Policy ## Delayed Orders Customers may request a full refund when an order has not been delivered within 7 calendar days after the promised delivery date. If the order is still in transit but has exceeded the 7-day grace period, the customer may choose either: - a full refund, or - a replacement shipment. A refund must not be issued automatically unless the order status has been verified. ## Damaged Products Customers who receive a damaged product must report the damage within 7 days of delivery. The customer may be asked to provide a photograph of the damaged product. Eligible damaged products may receive either a replacement or a full refund."""


async def main():

    embeddings = OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434",
        dimensions=1024,
    )

    lengths = [
        50,
        100,
        200,
        300,
        400,
        500,
        600,
        len(TEXT),
    ]

    for length in lengths:

        test_text = TEXT[:length]

        print()
        print(
            f"Testing {len(test_text)} characters..."
        )

        try:

            vector = await embeddings.aembed_query(
                test_text
            )

            print(
                "SUCCESS - dimensions:",
                len(vector)
            )

        except Exception as error:

            print("FAILED")
            print(error)

            # Stop because the Ollama model runner
            # may have crashed.
            break


asyncio.run(main())