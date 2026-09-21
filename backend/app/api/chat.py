from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.chat_repository import (
    add_message,
    get_recent_messages,
    get_session,
)
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
    db: AsyncSession = Depends(get_db),
):

    session= await get_session(
        db,
        request.session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )
    await add_message(
        db=db,
        session_id=request.session_id,
        role="user",
        content=request.message,
    )

    messages= await get_recent_messages(
        db=db,
        session_id=request.session_id,
        limit=10,
    )

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]

    try:
        response= await (
            llm_service.generate_response(history)
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        ) from exc

    await add_message(
        db=db,
        session_id=request.session_id,
        role="assistant",
        content=response,
    )

    return ChatResponse(
        session_id=request.session_id,
        response=response,
    )