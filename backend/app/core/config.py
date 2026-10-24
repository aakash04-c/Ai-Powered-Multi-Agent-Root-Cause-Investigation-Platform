from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Root Cause Investigation Platform"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # PostgreSQL database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_root_cause"

    # LLM Configuration (Sprint 2+)
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = "gemini-3.8-flash"
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
