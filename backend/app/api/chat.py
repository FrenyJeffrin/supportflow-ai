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
from app.schemas.chat import (ChatRequest, ChatResponse, SourceResponse)
from app.services.llm_service import LLMService
from app.rag.retrieval import retrieve_context

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
    db: AsyncSession = Depends(
        get_db
    ),
):

    session = await get_session(
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


    messages = (
        await get_recent_messages(
            db=db,
            session_id=request.session_id,
            limit=10,
        )
    )


    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]


    try:

        retrieved = await (retrieve_context(db=db, query=request.message,))

        context = "\n\n".join(
            [
                (
                    f"[Source: "
                    f"{item.title}]\n"
                    f"{item.content}"
                )
                for item in retrieved
            ]
        )


        response = await (llm_service.generate_response(history=history, context=context,))


    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=("AI service unavailable"),
        ) from exc


    await add_message(
        db=db,
        session_id=request.session_id,
        role="assistant",
        content=response,
    )

    unique_sources = {}

    for item in retrieved:

        if (item.source not in unique_sources):

            unique_sources[item.source] = SourceResponse(
                title=item.title,
                source=item.source,
                score=round(item.score, 3),
            )

    return ChatResponse(
        session_id=request.session_id,
        response=response,
        sources=list(unique_sources.values()),
    )