import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

from app.repositories.chat_repository import (
    create_session,
    get_messages,
    get_session,
    list_sessions,
)

from app.schemas.session import (
    MessageResponse,
    SessionResponse,
)

router= APIRouter(
    prefix="/api/v1/sessions",
    tags=["sessions"],
)

@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_session(
    db: AsyncSession = Depends(get_db),
):
    return await create_session(db)


@router.get(
    "",
    response_model= list[SessionResponse],
)
async def get_chat_sessions(
    db: AsyncSession = Depends(get_db),
):
    return await list_sessions(db)


@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
async def get_chat_session(
    session_id: uuid.UUID,
    db: AsyncSession= Depends(get_db),
):
    session= await get_session(
        db,
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )
    return session


@router.get(
    "/{session_id}/messages",
    response_model=list[MessageResponse],
)
async def get_session_messages(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    session= await get_session(
        db,
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    return await get_messages(
        db,
        session_id,
    )




 