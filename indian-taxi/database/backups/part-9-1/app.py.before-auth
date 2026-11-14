
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="INDIAN TAXI API",
    description="Professional Multi-Vehicle Ride-Hailing Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Development only
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/assets",
    StaticFiles(directory=FRONTEND_DIR / "assets"),
    name="assets"
)


@app.get("/")
async def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/v1/health")
async def health():
    return {
        "success": True,
        "project": "INDIAN TAXI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/v1/system")
async def system():
    return {
        "name": "INDIAN TAXI",
        "modules": [
            "Passenger",
            "Driver",
            "Admin",
            "Vehicles",
            "Bookings",
            "Payments",
            "Tracking"
        ],
        "status": "development"
    }
