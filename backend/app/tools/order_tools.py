import json

from langchain_core.tools import tool

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

    async with AsyncSessionLocal() as db:

        order = await find_order(
            db,
            order_number,
        )

        if order is None:

            return json.dumps({
                "found": False,
                "order_number": order_number,
            })

        return json.dumps({
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
                order.promised_delivery_date
                .isoformat()
            ),
            "delivered_at": (
                order.delivered_at.isoformat()
                if order.delivered_at
                else None
            ),
        })