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
    ollama_model: str = "gemma3:1b"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()