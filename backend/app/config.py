from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Price Tracker API"
    api_prefix: str = "/api/v1"
    debug: bool = False

    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/price_tracker"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 60

    etl_api_key: str = "change-me-etl-key"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"


settings = Settings()
