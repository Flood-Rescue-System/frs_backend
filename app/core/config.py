from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "Flood Detection API"
    DEBUG_MODE: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Model Settings
    DETECTION_CONFIDENCE_THRESHOLD: float = 0.5
    MAX_WATER_LEVEL_THRESHOLD: float = 30.0  # in cm
    CRITICAL_RISE_RATE: float = 5.0  # cm per minute
    
settings = Settings() 