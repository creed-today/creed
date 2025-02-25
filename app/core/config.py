from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    BINANCE_API_KEY: str
    BINANCE_API_SECRET: str
    COINGECKO_API_KEY: Optional[str] = None
    
    # Database
    DATABASE_URL: str
    
    # Model Settings
    MODEL_PATH: str = "models"
    PREDICTION_WINDOW: int = 24  # hours
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fluxion"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
