from fastapi import APIRouter
from app.schemas.chat import (ChatRequest, ChatResponse)
from app.services.llm_service import LLMService

router= APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

llm_service= LLMService()

@router.post(
    "",
    response_model=ChatResponse,
)

async def chat(
    request: ChatRequest,
):
    response= await llm_service.generate_response(request.message)
    return ChatResponse(response= response)