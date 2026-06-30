from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Ruta de la carpeta Backend
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )


settings = Settings()