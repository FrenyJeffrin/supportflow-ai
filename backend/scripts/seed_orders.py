import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Order


async def seed_orders():

    now = datetime.now(timezone.utc)

    orders = [
        {
            "order_number": "SF-1001",
            "customer_name": "Alex Johnson",
            "product_name": "Wireless Headphones",
            "amount": Decimal("89.99"),
            "status": "delivered",
            "promised_delivery_date": now - timedelta(days=5),
            "delivered_at": now - timedelta(days=4),
        },
        {
            "order_number": "SF-1002",
            "customer_name": "Priya Sharma",
            "product_name": "Mechanical Keyboard",
            "amount": Decimal("129.99"),
            "status": "in_transit",
            "promised_delivery_date": now - timedelta(days=10),
            "delivered_at": None,
        },
        {
            "order_number": "SF-1003",
            "customer_name": "Sam Wilson",
            "product_name": "USB-C Hub",
            "amount": Decimal("49.99"),
            "status": "processing",
            "promised_delivery_date": now + timedelta(days=4),
            "delivered_at": None,
        },
    ]

    async with AsyncSessionLocal() as db:

        for data in orders:

            result = await db.execute(
                select(Order).where(
                    Order.order_number
                    == data["order_number"]
                )
            )

            existing = (
                result.scalar_one_or_none()
            )

            if existing:
                print(
                    "Skipping:",
                    data["order_number"],
                )
                continue

            db.add(
                Order(**data)
            )

        await db.commit()

    print("Order seed complete.")


if __name__ == "__main__":

    asyncio.run(seed_orders())