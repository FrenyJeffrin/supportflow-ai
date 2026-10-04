from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order


async def find_order(
    db: AsyncSession,
    order_number: str,
) -> Order | None:

    result = await db.execute(
        select(Order).where(
            Order.order_number
            == order_number.upper()
        )
    )

    return result.scalar_one_or_none()