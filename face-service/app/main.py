from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import detection, recognition

app = FastAPI(
    title="FaceScan Face Recognition Service",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(detection.router, prefix="/api/v1/detection", tags=["detection"])
app.include_router(recognition.router, prefix="/api/v1/recognition", tags=["recognition"])

@app.get("/")
async def root():
    return {
        "message": "FaceScan Face Recognition Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
