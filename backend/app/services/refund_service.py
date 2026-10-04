from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, Refund


async def check_eligibility(
    order: Order,
) -> tuple[bool, str]:

    if order.status == "refunded":

        return (
            False,
            "Order has already been refunded.",
        )

    if order.status == "delivered":

        return (
            False,
            "Delivered orders are not eligible "
            "under the delayed-order rule.",
        )

    now = datetime.now(timezone.utc)

    promised = (order.promised_delivery_date)

    if promised.tzinfo is None:

        promised = promised.replace(tzinfo=timezone.utc)

    days_late = (now - promised).days

    if days_late < 7:

        return (
            False,
            (
                f"Order is only "
                f"{max(days_late, 0)} days late. "
                "Delayed-order refunds require "
                "at least 7 calendar days."
            ),
        )

    return (
        True,
        (
            f"Order is {days_late} days past "
            "the promised delivery date."
        ),
    )


async def create_refund(
    db: AsyncSession,
    order: Order,
) -> Refund:

    idempotency_key = (f"refund:{order.order_number}")

    result = await db.execute(
        select(Refund).where(
            Refund.idempotency_key
            == idempotency_key
        )
    )

    existing = (result.scalar_one_or_none())

    if existing:

        return existing

    refund = Refund(
        order_id=order.id,
        amount=order.amount,
        status="processed",
        idempotency_key=idempotency_key,
    )

    db.add(refund)

    order.status = "refunded"

    await db.commit()
    await db.refresh(refund)

    return refund