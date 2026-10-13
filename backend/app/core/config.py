from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SupportFlow AI"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_url: str =(
        "postgresql+asyncpg://" 
        "supportflow:devpassword@localhost:5432/supportflow"
    )

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3:4b"

    embedding_model: str = "nomic-embed-text"
    embedding_dimensions: int = 768

    rag_top_k: int = 4

    redis_url: str = ("redis://localhost:6379/0")

    celery_broker_url: str = ("redis://localhost:6379/1")

    celery_result_backend: str = ("redis://localhost:6379/2")

    order_cache_ttl: int = 2000

    chat_rate_limit: int = 20

    chat_rate_window_seconds: int = 60

model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()