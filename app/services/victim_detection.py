import cv2
import numpy as np
import torch
from ultralytics import YOLO
from datetime import datetime
from typing import Tuple, List, Optional
from app.core.config import settings

class VictimDetector:
    def __init__(self):
        # Initialize YOLO model
        self.model = YOLO('yolov8n.pt')  # Using nano model for speed
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def process_frame(self, frame_bytes) -> Tuple[List[dict], Optional[np.ndarray]]:
        """Process a frame and detect victims"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Run detection
            results = self.model(frame, conf=settings.DETECTION_CONFIDENCE_THRESHOLD)
            
            # Process results
            detections = []
            for r in results[0].boxes.data:
                x1, y1, x2, y2, conf, cls = r.tolist()
                if int(cls) == 0:  # class 0 is person in COCO dataset
                    detections.append({
                        'bbox': [float(x1), float(y1), float(x2), float(y2)],
                        'confidence': float(conf),
                        'class_name': 'person'
                    })
                    
                    # Draw bounding box on frame
                    cv2.rectangle(frame, 
                                (int(x1), int(y1)), 
                                (int(x2), int(y2)), 
                                (0, 255, 0), 2)
                    
                    # Add confidence score
                    text = f"Person: {conf:.2f}"
                    cv2.putText(frame, text, 
                              (int(x1), int(y1-10)), 
                              cv2.FONT_HERSHEY_SIMPLEX, 
                              0.5, (0, 255, 0), 2)
            
            return detections, frame
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return [], None
    
    def filter_detections(self, detections: List[dict]) -> List[dict]:
        """Filter out low confidence detections and apply NMS if needed"""
        filtered = [d for d in detections 
                   if d['confidence'] > settings.DETECTION_CONFIDENCE_THRESHOLD]
        return filtered 