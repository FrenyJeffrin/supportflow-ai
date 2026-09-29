import uuid
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    session_id: uuid.UUID

    message: str = Field(
        min_length=1,
        max_length=2000,
    )

class SourceResponse(BaseModel):
    title: str
    source: str
    score: float


class ChatResponse(BaseModel):
    session_id: uuid.UUID
    response: str
    sources: list[SourceResponse] = []