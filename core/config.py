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

    # Cosmos DB
    COSMOS_ENDPOINT: str = ""
    COSMOS_KEY: str = ""
    COSMOS_DATABASE: str = ""
    COSMOS_CONTAINER: str = ""
    COSMOS_SESSION_CONTAINER: str = ""

    # Azure AI Search
    AZURE_SEARCH_API_KEY: str = ""
    AZURE_SEARCH_ENDPOINT: str = ""
    AZURE_SEARCH_INDEX_NAME: str = ""
    AZURE_SEARCH_API_VERSION: str = ""

    # Azure Storage
    AZURE_STORAGE_ACCOUNT: str = ""
    AZURE_STORAGE_KEY: str = ""
    AZURE_STORAGE_CONTAINER: str = ""

    MODEL_NAME: str = "gpt-4.1-mini"
    TEMPERATURE: float = 0.3




    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()