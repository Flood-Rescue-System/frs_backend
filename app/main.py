from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import water_level, victim_detection

app = FastAPI(
    title=settings.APP_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    water_level.router,
    prefix=f"{settings.API_V1_STR}/water-level",
    tags=["Water Level Detection"]
)

app.include_router(
    victim_detection.router,
    prefix=f"{settings.API_V1_STR}/victim-detection",
    tags=["Victim Detection"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to Flood Detection API"} 