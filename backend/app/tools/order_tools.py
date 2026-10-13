import json

from langchain_core.tools import tool
from app.cache.order_cache import (
    cache_order,
    get_cached_order,
)
from app.database import AsyncSessionLocal
from app.services.order_service import (
    find_order,
)


@tool
async def get_order(
    order_number: str,
) -> str:
    """
    Look up an order using its order number.

    Use this whenever the customer asks about
    order status, delivery, product, or refund
    eligibility for a specific order.
    """

    print(
        f"[ORDER TOOL] called with: "
        f"{order_number!r}"
    )

    cached = await get_cached_order(
        order_number
    )

    if cached is not None:

        print(
            f"[CACHE HIT] "
            f"{order_number}"
        )

        cached["cache"] = "hit"

        return json.dumps(
            cached
        )
    print(
        f"[CACHE MISS] "
        f"{order_number}"
    )

    async with AsyncSessionLocal() as db:

        order = await find_order(
            db,
            order_number,
        )

        if order is None:

            print(
                f"[ORDER NOT FOUND] "
                f"{order_number}"
            )

            return json.dumps({
                "found": False,
                "order_number": order_number,
            })

        payload = {
            "found": True,
            "order_number": (
                order.order_number
            ),
            "product_name": (
                order.product_name
            ),
            "status": order.status,
            "amount": float(
                order.amount
            ),
            "promised_delivery_date": (
                order
                .promised_delivery_date
                .isoformat()
            ),
            "delivered_at": (
                order
                .delivered_at
                .isoformat()
                if order.delivered_at
                else None
            ),
        }
        print(
            f"[CACHE WRITE] "
            f"{order.order_number}"
        )

        await cache_order(
            order.order_number,
            payload,
        )

        print(
            f"[CACHE WRITE SUCCESS] "
            f"{order.order_number}"
        )

        payload["cache"] = "miss"


        return json.dumps(
            payload
        )
    