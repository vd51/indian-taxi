from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.core.config import settings
from backend.core.database import init_db
from backend.api.auth import router as auth_router

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="INDIAN TAXI API", description="Professional Multi-Vehicle Ride-Hailing Platform", version="1.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# 1. API પહેલા - હંમેશા API પહેલા, Static પછી
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Passenger Authentication"])

@app.on_event("startup")
def startup_event(): init_db()

@app.get("/api/v1/health")
async def health():
    return {"success": True, "project": "INDIAN TAXI", "status": "running", "version": "1.1.0"}

@app.get("/api/v1/system")
async def system():
    return {"name": "INDIAN TAXI", "modules": ["Passenger","Driver","Admin","Vehicles","Bookings","Payments","Tracking","Authentication"], "status": "development"}

@app.get("/api/v1/dashboard")
async def dashboard():
    # Passenger Dashboard API - Real Data
    from backend.core.database import DB_PATH
    import sqlite3
    db = sqlite3.connect(DB_PATH); db.row_factory = sqlite3.Row
    total_users = db.execute("SELECT COUNT(*) as c FROM users").fetchone()["c"]
    total_bookings = db.execute("SELECT COUNT(*) as c FROM bookings").fetchone()["c"]
    return {"success": True, "total_users": total_users, "total_bookings": total_bookings, "wallet": 250, "history": [{"pickup":"Daman","drop":"Vapi","fare":180,"vehicle":"AUTO"}]}

# 2. Static - Assets / Auth - API પછી
app.mount("/assets", StaticFiles(directory=FRONTEND_DIR / "assets"), name="assets")
app.mount("/auth", StaticFiles(directory=FRONTEND_DIR / "auth"), name="auth")

@app.get("/")
async def home(): return FileResponse(FRONTEND_DIR / "index.html")

# 3. Frontend - છેલ્લે જ - આનાથી API દબાતું નથી
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
