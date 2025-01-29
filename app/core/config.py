from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Flood Detection API"
    DEBUG_MODE: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Model Settings
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.5
    MAX_WATER_LEVEL_THRESHOLD: float = 30.0  # in cm
    CRITICAL_RISE_RATE: float = 5.0  # cm per minute
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 