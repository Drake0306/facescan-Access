from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio

from app.core.config import settings
from app.api.routes import auth, visitors, visits, gate, reports

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO setup
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ORIGINS
)
socket_app = socketio.ASGIApp(sio, app)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(visitors.router, prefix=f"{settings.API_V1_STR}/visitors", tags=["visitors"])
app.include_router(visits.router, prefix=f"{settings.API_V1_STR}/visits", tags=["visits"])
app.include_router(gate.router, prefix=f"{settings.API_V1_STR}/gate", tags=["gate"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])

@app.get("/")
async def root():
    return {
        "message": "FaceScan Access API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Socket.IO events
@sio.event
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")
    # TODO: Verify JWT token from auth

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Export for use in other modules
def get_sio():
    return sio
