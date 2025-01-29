from fastapi import APIRouter, UploadFile, File, WebSocket, HTTPException
from app.core.models import WaterLevelData, WaterLevelResponse
from app.services.water_detection import WaterLevelDetector
import cv2
import asyncio
from datetime import datetime

router = APIRouter()
detector = WaterLevelDetector()

@router.post("/process-frame")
async def process_frame(file: UploadFile = File(...), location_id: str = None):
    """Process a single frame for water level detection"""
    try:
        contents = await file.read()
        water_level, processed_frame = detector.process_frame(contents)
        
        if water_level is None:
            raise HTTPException(status_code=400, detail="Could not detect water level")
        
        is_critical = detector.check_critical_level(water_level, location_id)
        
        return WaterLevelResponse(
            level=water_level,
            status="critical" if is_critical else "normal",
            is_critical=is_critical,
            timestamp=datetime.now(),
            location_id=location_id,
            alert_message="Critical water level detected!" if is_critical else None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{location_id}")
async def websocket_endpoint(websocket: WebSocket, location_id: str):
    """WebSocket endpoint for real-time water level detection"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_bytes()
            water_level, processed_frame = detector.process_frame(data)
            
            if water_level is not None:
                is_critical = detector.check_critical_level(water_level, location_id)
                
                response = WaterLevelResponse(
                    level=water_level,
                    status="critical" if is_critical else "normal",
                    is_critical=is_critical,
                    timestamp=datetime.now(),
                    location_id=location_id,
                    alert_message="Critical water level detected!" if is_critical else None
                )
                
                await websocket.send_json(response.dict())
            
            await asyncio.sleep(0.1)  # Prevent overwhelming the connection
            
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close() 