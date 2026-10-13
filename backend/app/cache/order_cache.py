import json

from app.cache.redis_client import (
    redis_client,
)

from app.core.config import settings
from app.observability.metrics import (
    CACHE_HITS,
    CACHE_MISSES,
)


def order_cache_key(
    order_number: str,
) -> str:

    return (
        f"supportflow:"
        f"order:"
        f"{order_number.upper()}"
    )


async def get_cached_order(
    order_number: str,
) -> dict | None:

    value = await redis_client.get(
        order_cache_key(
            order_number
        )
    )

    if value is None:

       CACHE_MISSES.labels(cache="order").inc()

       return None

    CACHE_HITS.labels(cache="order").inc()

    return json.loads(value)


async def cache_order(
    order_number: str,
    data: dict,
):

    # await redis_client.set(
    #     order_cache_key(
    #         order_number
    #     ),
    #     json.dumps(data),
    #     ex=settings.order_cache_ttl,
    # )

    key = order_cache_key(
        order_number
    )

    print(
        f"[REDIS WRITE] key={key}"
    )

    result = await redis_client.set(
        key,
        json.dumps(data),
        ex=settings.order_cache_ttl,
    )

    print(
        f"[REDIS SET RESULT] {result}"
    )

    value = await redis_client.get(
        key
    )

    print(
        f"[REDIS IMMEDIATE GET] {value}"
    )

    ttl = await redis_client.ttl(
        key
    )

    print(
        f"[REDIS IMMEDIATE TTL] {ttl}"
    )


async def invalidate_order(
    order_number: str,
):

    await redis_client.delete(
        order_cache_key(
            order_number
        )
    )