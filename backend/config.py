from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str

    qdrant_url: str

    qdrant_api_key: str | None = None

    collection_name: str

    embedding_model: str

    llm_model: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()