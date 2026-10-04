import json

from langchain_core.tools import tool

from app.database import AsyncSessionLocal

from app.models import SupportTicket

from app.services.order_service import (
    find_order,
)


@tool
async def create_support_ticket(
    order_number: str,
    reason: str,
) -> str:
    """
    Create a human-support ticket when an issue
    cannot be resolved automatically.

    Use this when escalation is appropriate.
    """

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

        ticket = SupportTicket(
            order_id=order.id,
            reason=reason,
            status="open",
        )

        db.add(ticket)

        await db.commit()
        await db.refresh(ticket)

        return json.dumps({
            "success": True,
            "ticket_id": str(
                ticket.id
            ),
            "status": ticket.status,
            "order_number": (
                order.order_number
            ),
        })