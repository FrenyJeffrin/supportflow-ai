import asyncio

from langchain_ollama import OllamaEmbeddings


async def main():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434",
        dimensions=768,
    )

    texts = [
        "Customers may request a refund for a delayed order.",
        "Refund requests must be submitted within the eligible period.",
    ]

    print("Sending 2 documents to Ollama...")

    vectors = await embeddings.aembed_documents(texts)

    print("SUCCESS")
    print("Number of vectors:", len(vectors))
    print("Vector dimensions:", len(vectors[0]))


asyncio.run(main())