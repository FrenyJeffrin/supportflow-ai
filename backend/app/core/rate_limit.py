import uuid

from app.cache.redis_client import (
    redis_client,
)

from app.core.config import settings


async def check_chat_rate_limit(
    session_id: uuid.UUID,
) -> tuple[bool, int]:

    key = (
        "supportflow:"
        "rate:"
        "chat:"
        f"{session_id}"
    )

    count = await redis_client.incr(
        key
    )

    if count == 1:

        await redis_client.expire(
            key,
            settings
            .chat_rate_window_seconds,
        )


    allowed = (
        count
        <= settings.chat_rate_limit
    )


    return (
        allowed,
        int(count),
    )