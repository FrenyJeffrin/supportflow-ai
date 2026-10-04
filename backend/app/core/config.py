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

model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()