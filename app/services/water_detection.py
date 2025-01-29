import cv2
import numpy as np
from datetime import datetime
from app.core.config import settings

class WaterLevelDetector:
    def __init__(self):
        self.previous_levels = {}  # Store previous levels for rate calculation
        
    def process_frame(self, frame_bytes, roi_coords=None):
        """Process a frame and detect water level"""
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Use default ROI if none provided
            if roi_coords is None:
                height, width = frame.shape[:2]
                roi_coords = (0, height, width//4, width//2)
            
            # Extract ROI and process
            y1, y2, x1, x2 = roi_coords
            roi = frame[y1:y2, x1:x2]
            
            # Convert to grayscale and apply preprocessing
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)
            
            # Detect lines
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, 15, 
                                  minLineLength=50, maxLineGap=20)
            
            if lines is None:
                return None, frame
                
            # Find water level (average of lowest detected lines)
            lowest_lines = sorted(lines, key=lambda x: (x[0][1] + x[0][3])/2)[-3:]
            water_level = int(np.mean([((line[0][1] + line[0][3])/2) for line in lowest_lines]))
            
            # Draw detection on frame
            cv2.line(frame, (x1, water_level + y1), (x2, water_level + y1), 
                    (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Convert water level to cm (using calibration)
            water_level_cm = self._pixel_to_cm(water_level)
            
            return water_level_cm, frame
            
        except Exception as e:
            print(f"Error processing frame: {str(e)}")
            return None, None
    
    def _pixel_to_cm(self, pixel_value):
        """Convert pixel value to centimeters using calibration"""
        # This is a simplified conversion - adjust based on your calibration
        return pixel_value * 0.1  # Example conversion factor
    
    def check_critical_level(self, level: float, location_id: str) -> bool:
        """Check if water level is critical"""
        now = datetime.now()
        
        # Store current level and time
        if location_id in self.previous_levels:
            prev_level, prev_time = self.previous_levels[location_id]
            time_diff = (now - prev_time).total_seconds() / 60  # Convert to minutes
            
            if time_diff > 0:
                rise_rate = (level - prev_level) / time_diff
                is_critical = (rise_rate > settings.CRITICAL_RISE_RATE or 
                             level > settings.MAX_WATER_LEVEL_THRESHOLD)
            else:
                is_critical = level > settings.MAX_WATER_LEVEL_THRESHOLD
        else:
            is_critical = level > settings.MAX_WATER_LEVEL_THRESHOLD
        
        self.previous_levels[location_id] = (level, now)
        return is_critical 