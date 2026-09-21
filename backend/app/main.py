from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.chat import router as chat_router
from app.database import get_db
from app.api.sessions import router as sessions_router

app = FastAPI(
    title="SupportFlow AI API",
    description=("Backend API for the SupportFlow AI"
                  " customer support agent"
                  ),
    version="0.1.0",
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
        "databse": "connected",
        "result": result.scalar(),
    }