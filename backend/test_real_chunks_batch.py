import asyncio
from pathlib import Path

from langchain_ollama import OllamaEmbeddings

from app.rag.chunker import chunk_text


async def main():

    file_path = (
        Path(__file__).resolve().parent.parent
        / "knowledge"
        / "refund_policy.md"
    )

    text = file_path.read_text(
        encoding="utf-8"
    )

    chunks = chunk_text(text)

    print("Number of chunks:", len(chunks))

    for index, chunk in enumerate(chunks):
        print(
            f"Chunk {index}: "
            f"{len(chunk)} characters"
        )

    embeddings = OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434",
        dimensions=1024,
    )

    print()
    print("Sending BOTH real chunks together...")

    vectors = await embeddings.aembed_documents(
        chunks
    )

    print()
    print("SUCCESS")
    print("Vectors:", len(vectors))

    for index, vector in enumerate(vectors):
        print(
            f"Vector {index}: "
            f"{len(vector)} dimensions"
        )


asyncio.run(main())