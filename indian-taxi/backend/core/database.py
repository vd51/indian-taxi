import sqlite3
from pathlib import Path
from backend.core.config import settings
DB_PATH = Path(__file__).resolve().parent.parent.parent / settings.DATABASE_PATH

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY, full_name TEXT NOT NULL, phone TEXT UNIQUE NOT NULL,
        email TEXT, password_hash TEXT NOT NULL, role TEXT DEFAULT 'passenger',
        is_verified INTEGER DEFAULT 0, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS passengers (
        id TEXT PRIMARY KEY, user_id TEXT UNIQUE NOT NULL, wallet_balance REAL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    CREATE TABLE IF NOT EXISTS otp_challenges (
        id TEXT PRIMARY KEY, phone TEXT NOT NULL, purpose TEXT NOT NULL,
        otp_hash TEXT NOT NULL, payload_json TEXT, attempts INTEGER DEFAULT 0,
        expires_at TEXT NOT NULL, consumed_at TEXT, created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS auth_sessions (
        id TEXT PRIMARY KEY, user_id TEXT NOT NULL, expires_at TEXT NOT NULL,
        created_at TEXT NOT NULL, last_seen_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS bookings (
        id TEXT PRIMARY KEY, passenger_id TEXT, pickup TEXT, drop_loc TEXT,
        vehicle TEXT DEFAULT 'AUTO', fare REAL DEFAULT 0, status TEXT DEFAULT 'BOOKED',
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS payments (
        id TEXT PRIMARY KEY, booking_id TEXT, method TEXT DEFAULT 'UPI',
        amount REAL DEFAULT 0, status TEXT DEFAULT 'PAID', created_at TEXT NOT NULL
    );
    """)
    db.commit(); db.close()
    print(f"Database Ready: {DB_PATH}")
