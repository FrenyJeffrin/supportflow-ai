import json

from langchain_core.tools import tool

from app.database import AsyncSessionLocal

from app.services.order_service import (
    find_order,
)

from app.services.refund_service import (
    check_eligibility,
    create_refund,
)

@tool
async def check_refund_eligibility(
    order_number: str,
) -> str:
    """
    Check whether an order qualifies for a
    delayed-delivery refund.

    This tool only checks eligibility.
    It does NOT issue a refund.
    """

    async with AsyncSessionLocal() as db:

        order = await find_order(
            db,
            order_number,
        )

        if order is None:

            return json.dumps({
                "eligible": False,
                "reason": "Order not found.",
            })

        eligible, reason = (
            await check_eligibility(
                order
            )
        )

        return json.dumps({
            "order_number": (
                order.order_number
            ),
            "eligible": eligible,
            "reason": reason,
            "amount": float(
                order.amount
            ),
        })

@tool
async def process_refund(
    order_number: str,
    confirmed: bool,
) -> str:
    """
    Process a refund for an eligible order.

    Only call this when the customer has
    explicitly confirmed that they want the
    refund processed.

    confirmed must be true.
    """

    if not confirmed:

        return json.dumps({
            "success": False,
            "requires_confirmation": True,
            "message": (
                "Explicit customer "
                "confirmation is required."
            ),
        })

    async with AsyncSessionLocal() as db:

        order = await find_order(
            db,
            order_number,
        )

        if order is None:

            return json.dumps({
                "success": False,
                "message": "Order not found.",
            })

        eligible, reason = (
            await check_eligibility(
                order
            )
        )

        if not eligible:

            return json.dumps({
                "success": False,
                "message": reason,
            })

        refund = await create_refund(
            db,
            order,
        )

        return json.dumps({
            "success": True,
            "refund_id": str(
                refund.id
            ),
            "order_number": (
                order.order_number
            ),
            "amount": float(
                refund.amount
            ),
            "status": refund.status,
        })