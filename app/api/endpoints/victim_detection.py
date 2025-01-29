from fastapi import APIRouter, UploadFile, File, WebSocket, HTTPException
from app.core.models import VictimDetectionResponse, Detection
from app.services.victim_detection import VictimDetector
import cv2
import asyncio
from datetime import datetime

router = APIRouter()
detector = VictimDetector()

@router.post("/process-frame")
async def process_frame(file: UploadFile = File(...), location_id: str = None):
    """Process a single frame for victim detection"""
    try:
        contents = await file.read()
        detections, processed_frame = detector.process_frame(contents)
        
        if detections is None:
            raise HTTPException(status_code=400, detail="Could not process frame")
        
        # Filter and convert detections
        filtered_detections = [
            Detection(
                bbox=d['bbox'],
                confidence=d['confidence'],
                class_name=d['class_name']
            ) for d in detector.filter_detections(detections)
        ]
        
        return VictimDetectionResponse(
            timestamp=datetime.now(),
            location_id=location_id,
            detections=filtered_detections,
            total_victims=len(filtered_detections)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{location_id}")
async def websocket_endpoint(websocket: WebSocket, location_id: str):
    """WebSocket endpoint for real-time victim detection"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_bytes()
            detections, processed_frame = detector.process_frame(data)
            
            if detections is not None:
                filtered_detections = [
                    Detection(
                        bbox=d['bbox'],
                        confidence=d['confidence'],
                        class_name=d['class_name']
                    ) for d in detector.filter_detections(detections)
                ]
                
                response = VictimDetectionResponse(
                    timestamp=datetime.now(),
                    location_id=location_id,
                    detections=filtered_detections,
                    total_victims=len(filtered_detections)
                )
                
                await websocket.send_json(response.dict())
            
            await asyncio.sleep(0.1)  # Prevent overwhelming the connection
            
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
    finally:
        await websocket.close() 