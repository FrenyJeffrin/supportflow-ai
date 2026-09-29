def chunk_text(
    text: str,
    chunk_size: int = 700,
    overlap: int = 120,
) -> list[str]:

    cleaned = " ".join(
        text.split()
    )


    if not cleaned:
        return []


    chunks: list[str] = []

    start = 0

    text_length = len(cleaned)


    while start < text_length:

        end = min(
            start + chunk_size,
            text_length,
        )


        if end < text_length:

            boundary = cleaned.rfind(
                ". ",
                start,
                end,
            )

            if boundary > start + (
                chunk_size // 2
            ):

                end = boundary + 1


        chunk = cleaned[
            start:end
        ].strip()


        if chunk:
            chunks.append(chunk)


        if end >= text_length:
            break


        start = max(
            end - overlap,
            start + 1,
        )


    return chunks