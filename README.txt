FLOOD DETECTION API
==================

A FastAPI-based backend service that provides real-time water level detection and flood victim detection using computer vision.

Features:
---------
1. Water Level Detection
   - Real-time water level measurement from video feeds
   - Critical level alerts
   - Support for multiple locations
   - Both REST API and WebSocket endpoints

2. Victim Detection
   - Real-time person detection in flood scenarios
   - Multiple person tracking
   - Confidence scores for each detection
   - Both REST API and WebSocket endpoints

Deployment Steps:
----------------
1. GitHub Deployment:
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/flood-detection-api.git
   git push -u origin main

2. Render Deployment:
   a. Go to render.com and sign up/login
   b. Click "New +" and select "Web Service"
   c. Connect your GitHub repository
   d. Configure the service:
      - Name: flood-detection-api
      - Environment: Python 3
      - Build Command: pip install -r requirements.txt
      - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   e. Click "Create Web Service"

API Usage:
----------
Base URL: https://your-render-url.onrender.com/api/v1

1. Water Level Detection:

   a. Single Frame Processing:
   Endpoint: POST /water-level/process-frame
   Parameters:
   - file: Image file (multipart/form-data)
   - location_id: String (query parameter)

   Example (Next.js):
   const formData = new FormData();
   formData.append('file', imageFile);
   
   const response = await fetch(
     `${API_URL}/water-level/process-frame?location_id=location1`,
     {
       method: 'POST',
       body: formData
     }
   );
   const data = await response.json();
   // data contains: {level, status, is_critical, timestamp, location_id, alert_message}

   b. Real-time WebSocket:
   Endpoint: ws://your-render-url.onrender.com/api/v1/water-level/ws/{location_id}

   Example (Next.js):
   const ws = new WebSocket(
     `ws://your-render-url.onrender.com/api/v1/water-level/ws/location1`
   );
   
   ws.onmessage = (event) => {
     const data = JSON.parse(event.data);
     // Update UI with water level data
   };

2. Victim Detection:

   a. Single Frame Processing:
   Endpoint: POST /victim-detection/process-frame
   Parameters:
   - file: Image file (multipart/form-data)
   - location_id: String (query parameter)

   Example (Next.js):
   const formData = new FormData();
   formData.append('file', imageFile);
   
   const response = await fetch(
     `${API_URL}/victim-detection/process-frame?location_id=location1`,
     {
       method: 'POST',
       body: formData
     }
   );
   const data = await response.json();
   // data contains: {timestamp, location_id, detections, total_victims}

   b. Real-time WebSocket:
   Endpoint: ws://your-render-url.onrender.com/api/v1/victim-detection/ws/{location_id}

   Example (Next.js):
   const ws = new WebSocket(
     `ws://your-render-url.onrender.com/api/v1/victim-detection/ws/location1`
   );
   
   ws.onmessage = (event) => {
     const data = JSON.parse(event.data);
     // Update UI with detection data
     // data.detections contains array of detected persons with bounding boxes
   };

Response Formats:
----------------
1. Water Level Response:
{
    "level": float,            // Water level in cm
    "status": string,          // "normal" or "critical"
    "is_critical": boolean,    // true if level is critical
    "timestamp": string,       // ISO format timestamp
    "location_id": string,     // Location identifier
    "alert_message": string    // Optional alert message
}

2. Victim Detection Response:
{
    "timestamp": string,       // ISO format timestamp
    "location_id": string,     // Location identifier
    "detections": [           // Array of detections
        {
            "bbox": [x1, y1, x2, y2],  // Bounding box coordinates
            "confidence": float,        // Detection confidence
            "class_name": "person"      // Always "person"
        }
    ],
    "total_victims": integer   // Total number of detected persons
}

Notes:
------
1. For production deployment, update CORS settings in main.py
2. Adjust detection thresholds in config.py if needed
3. The WebSocket connections automatically handle reconnection
4. For high-traffic scenarios, consider using a load balancer
5. Monitor your Render usage as ML processing can be resource-intensive 