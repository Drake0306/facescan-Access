from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import gate

app = FastAPI(
    title="FaceScan Gate Controller Service",
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
app.include_router(gate.router, prefix="/api/v1/gate", tags=["gate"])

@app.get("/")
async def root():
    return {
        "message": "FaceScan Gate Controller Service",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
