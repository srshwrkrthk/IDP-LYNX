from fastapi import FastAPI

from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="LYNX GATEWAY API",
    description="Software-first HID security and SOC platform",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "name": "LYNX",
        "status": "running",
        "mode": "software-mock",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}