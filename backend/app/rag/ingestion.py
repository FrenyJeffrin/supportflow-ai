import asyncio
import hashlib
from pathlib import Path

from sqlalchemy import delete, select

from app.database import AsyncSessionLocal

from app.models import (
    DocumentChunk,
    KnowledgeDocument,
)

from app.rag.chunker import chunk_text

from app.rag.embeddings import (
    embedding_service,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parents[3]


KNOWLEDGE_DIR = (
    PROJECT_ROOT / "knowledge"
)


async def ingest_file(
    file_path: Path,
):

    text = file_path.read_text(
        encoding="utf-8"
    )


    content_hash = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


    source = file_path.name

    title = (
        file_path.stem
        .replace("_", " ")
        .title()
    )


    async with AsyncSessionLocal() as db:

        statement = select(
            KnowledgeDocument
        ).where(
            KnowledgeDocument.source
            == source
        )


        result = await db.execute(
            statement
        )


        existing = (
            result.scalar_one_or_none()
        )


        if (
            existing is not None
            and
            existing.content_hash
            == content_hash
        ):

            print(
                f"Skipping unchanged: "
                f"{source}"
            )

            return


        if existing is not None:

            await db.execute(
                delete(
                    KnowledgeDocument
                ).where(
                    KnowledgeDocument.id
                    == existing.id
                )
            )

            await db.commit()


        chunks = chunk_text(text)


        if not chunks:

            print(
                f"No content: {source}"
            )

            return


        print(
            f"Embedding {source}: "
            f"{len(chunks)} chunks"
        )

        for i, chunk in enumerate(chunks):
          print(f"Chunk {i}: {len(chunk)} characters")
          
        vectors = await (
            embedding_service
            .embed_documents(chunks)
        )


        document = KnowledgeDocument(
            title=title,
            source=source,
            content_hash=content_hash,
        )


        db.add(document)

        await db.flush()


        for index, (
            chunk,
            vector,
        ) in enumerate(
            zip(
                chunks,
                vectors,
                strict=True,
            )
        ):

            db.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding=vector,
                )
            )


        await db.commit()


        print(
            f"Ingested: {source}"
        )


async def ingest_all():

    files = sorted(
        KNOWLEDGE_DIR.glob("*.md")
    )


    if not files:

        print(
            "No knowledge files found."
        )

        return


    for file_path in files:

        await ingest_file(
            file_path
        )


if __name__ == "__main__":

    asyncio.run(
        ingest_all()
    )