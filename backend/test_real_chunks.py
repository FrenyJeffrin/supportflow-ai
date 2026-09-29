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

    print("Reading:", file_path)

    text = file_path.read_text(
        encoding="utf-8"
    )

    chunks = chunk_text(text)

    print("Chunks:", len(chunks))

    embeddings = OllamaEmbeddings(
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434",
        dimensions=1024,
    )

    for index, chunk in enumerate(chunks):

        print()
        print(
            f"Testing chunk {index}: "
            f"{len(chunk)} characters"
        )


        print("----- CHUNK CONTENT -----")
        print(repr(chunk))
        print("-------------------------")

        try:
            vectors = await embeddings.aembed_documents(
                [chunk]
            )

            print(
                f"Chunk {index}: SUCCESS"
            )

            print(
                "Dimensions:",
                len(vectors[0])
            )

        except Exception as error:

            print(
                f"Chunk {index}: FAILED"
            )

            print(error)

            break


asyncio.run(main())