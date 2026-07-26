from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "DocuMind"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Enterprise Document Intelligence Platform"

    DEBUG: bool = False

    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "documind"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()