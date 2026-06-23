import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    ALPHA_VANTAGE_KEY: str
    
    TRACKED_ASSETS: list[dict] = [
        {"type": "stock", "symbol": "IBM"},
        {"type": "crypto", "id": "bitcoin"},
        {"type": "fiat", "base": "USD", "target": "EUR"}
    ]

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, 
        env_file_encoding='utf-8', 
        extra="ignore"
    )

settings = Settings()