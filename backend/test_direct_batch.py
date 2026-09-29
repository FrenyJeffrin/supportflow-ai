import json
import urllib.request
from pathlib import Path

from app.rag.chunker import chunk_text


file_path = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "refund_policy.md"
)

text = file_path.read_text(
    encoding="utf-8"
)

chunks = chunk_text(text)

print("Chunks:", len(chunks))

for index, chunk in enumerate(chunks):
    print(
        f"Chunk {index}: "
        f"{len(chunk)} characters"
    )


payload = {
    "model": "qwen3-embedding:0.6b",
    "input": chunks,
}


data = json.dumps(payload).encode(
    "utf-8"
)


request = urllib.request.Request(
    "http://localhost:11434/api/embed",
    data=data,
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)


print()
print("Sending exact real chunks directly to Ollama...")


with urllib.request.urlopen(
    request,
    timeout=120,
) as response:

    result = json.loads(
        response.read().decode("utf-8")
    )


print("SUCCESS")
print(
    "Vectors:",
    len(result["embeddings"])
)

print(
    "Dimensions:",
    len(result["embeddings"][0])
)