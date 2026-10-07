from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes.auth import router as auth_router
from app.api.routes.devices import router as devices_router
from app.api.routes.events import router as events_router

frontend = Path(__file__).resolve().parents[2] / "frontend"

app = FastAPI(
    title="LYNX GATEWAY API",
    description="Software-first USB security and SOC platform",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(events_router)

app.mount(
    "/static",
    StaticFiles(directory=frontend / "css"),
    name="static",
)


@app.get("/", include_in_schema=False)
def login_page():
    return FileResponse(frontend / "index.html")


@app.get("/dashboard", include_in_schema=False)
def dashboard_page():
    return FileResponse(frontend / "dashboard.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}