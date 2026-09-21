import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatSession, Message

async def create_session(
        db: AsyncSession,
) -> ChatSession:

    session= ChatSession()

    db.add(session)

    await db.commit()
    await db.refresh(session)

    return session

async def get_session(
        db: AsyncSession,
        session_id: uuid.UUID,
) -> ChatSession | None:

    statement = select(ChatSession).where(
        ChatSession.id == session_id
    )

    result= await db.execute(statement)

    return result.scalar_one_or_none()

async def list_sessions(
        db: AsyncSession,
        limit: int=20,
) -> list[ChatSession]:

    statement= (
        select(ChatSession)
        .order_by(ChatSession.updated_at.desc())
        .limit(limit)
    )

    result= await db.execute(statement)

    return list(result.scalars().all())

async def add_message(
        db: AsyncSession,
        session_id: uuid.UUID,
        role: str,
        content:str,
) -> Message:

    message= Message(
        session_id= session_id,
        role= role,
        content= content,
    )

    db.add(message)

    session= await get_session(
        db,
        session_id,
    )

    if session:
        session.title =(
            session.title
            if session.title != "New conversation"
            else content[:60]
        )

    await db.commit()
    await db.refresh(message)

    return message

async def get_messages(
        db: AsyncSession,
        session_id: uuid.UUID,
        limit: int = 100,
) -> list[Message]:

    statement= (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.asc(), Message.id.asc(),)
        .limit(limit)
    )

    result = await db.execute(statement)
    return list(result.scalars().all())

async def get_recent_messages(
        db: AsyncSession,
        session_id: uuid.UUID,
        limit: int = 10,
) -> list[Message]:

    statement = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.created_at.desc(), Message.id.desc(),)
        .limit(limit)
    )

    result= await db.execute(statement)
    messages= list(result.scalars().all())
    messages.reverse()
    return messages

    
