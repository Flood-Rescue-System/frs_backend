from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class WaterLevelData(BaseModel):
    level: float = Field(..., description="Water level in centimeters")
    timestamp: datetime = Field(default_factory=datetime.now)
    location_id: str = Field(..., description="Unique identifier for the location")
    
class WaterLevelResponse(BaseModel):
    level: float
    status: str
    is_critical: bool
    timestamp: datetime
    location_id: str
    alert_message: Optional[str] = None

class Frame(BaseModel):
    data: bytes
    timestamp: datetime = Field(default_factory=datetime.now)
    location_id: str

class Detection(BaseModel):
    bbox: List[float]  # [x1, y1, x2, y2]
    confidence: float
    class_name: str = "person"

class VictimDetectionResponse(BaseModel):
    timestamp: datetime
    location_id: str
    detections: List[Detection]
    total_victims: int
    processed_frame_url: Optional[str] = None 