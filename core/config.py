from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    # OpenAI
    OPENAI_API_KEY: str
    MODEL_NAME: str
    TEMPERATURE: float = 0

    # Redis
    REDIS_CONNECTION_STRING: str | None = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # API Security
    API_KEY: str

    # Azure Monitoring
    APPLICATIONINSIGHTS_CONNECTION_STRING: (
        str | None
    ) = None

    # Azure Search
    AZURE_SEARCH_ENDPOINT: str | None = None
    AZURE_SEARCH_KEY: str | None = None
    AZURE_SEARCH_INDEX_NAME: str | None = None
    AZURE_SEARCH_API_VERSION: (
        str | None
    ) = None

    # Feature Flags
    ENABLE_INGESTION: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()