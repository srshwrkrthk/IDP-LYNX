from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.devices import router as devices_router
from app.api.routes.events import router as events_router

app = FastAPI(
    title="LYNX GATEWAY API",
    description="Software-first USB security and SOC platform",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(events_router)

@app.get("/")
def root():
    return {
        "name": "LYNX Gateway API",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}