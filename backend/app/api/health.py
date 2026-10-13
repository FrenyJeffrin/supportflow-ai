from sqlalchemy import text

from app.cache.redis_client import (
    check_redis,
)
from fastapi import (
    APIRouter,
    HTTPException,
)
from app.database import AsyncSessionLocal

router = APIRouter(tags=["Health"])

@router.get("/live")
async def liveness():
    return {
        "status": "alive"
    }

@router.get("/ready")
async def readiness():

    postgres_ok = False

    redis_ok = await check_redis()


    try:

        async with (
            AsyncSessionLocal()
            as db
        ):

            await db.execute(
                text("SELECT 1")
            )

            postgres_ok = True

    except Exception:

        postgres_ok = False


    ready = (
        postgres_ok
        and redis_ok
    )

    if not ready:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "not_ready",
                "dependencies": {
                    "postgres": postgres_ok,
                    "redis": redis_ok,
                },
            },
        )

    return {
        "status": (
            "ready"
            if ready
            else "not_ready"
        ),
        "dependencies": {
            "postgres": (
                postgres_ok
            ),
            "redis": redis_ok,
        },
    }