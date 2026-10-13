from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.chat import router as chat_router
from app.database import get_db
from app.api.sessions import router as sessions_router
from prometheus_client import (
    make_asgi_app,
)
import time

from fastapi import Request

from app.observability.metrics import (
    HTTP_LATENCY,
    HTTP_REQUESTS,
)
from app.api.health import router as health_router

from app.core.logging_config import (
    configure_logging,
)

configure_logging()

app = FastAPI(
    title="SupportFlow AI API",
    description=("Backend API for the SupportFlow AI"
                  " customer support agent"
                  ),
    version="0.1.0",
)

metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(sessions_router)
app.include_router(health_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to SupportFlow AI API"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "supportflow-api",
    }


@app.get("/health/db")
async def database_health(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }

@app.middleware("http")
async def metrics_middleware(
    request: Request,
    call_next,
):

    start = time.perf_counter()

    response = await call_next(
        request
    )

    duration = (
        time.perf_counter()
        - start
    )

    path = request.url.path

    HTTP_REQUESTS.labels(
        method=request.method,
        path=path,
        status=str(
            response.status_code
        ),
    ).inc()

    HTTP_LATENCY.labels(
        method=request.method,
        path=path,
    ).observe(duration)

    return response