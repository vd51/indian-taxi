PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    role TEXT NOT NULL DEFAULT 'passenger'
        CHECK(role IN ('passenger', 'driver', 'admin')),

    phone TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK(is_active IN (0, 1)),

    is_verified INTEGER NOT NULL DEFAULT 0
        CHECK(is_verified IN (0, 1)),

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS passenger_profiles (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,

    full_name TEXT NOT NULL,
    profile_photo TEXT,
    emergency_contact TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS otp_challenges (
    id TEXT PRIMARY KEY,
    phone TEXT NOT NULL,
    purpose TEXT NOT NULL
        CHECK(purpose IN ('registration')),

    otp_hash TEXT NOT NULL,
    payload_json TEXT NOT NULL,

    attempts INTEGER NOT NULL DEFAULT 0,
    expires_at TEXT NOT NULL,
    consumed_at TEXT,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_otp_phone_created
ON otp_challenges(phone, created_at);

CREATE INDEX IF NOT EXISTS idx_otp_expiry
ON otp_challenges(expires_at);

CREATE TABLE IF NOT EXISTS auth_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,

    expires_at TEXT NOT NULL,
    revoked_at TEXT,

    created_at TEXT NOT NULL,
    last_seen_at TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user
ON auth_sessions(user_id);

CREATE INDEX IF NOT EXISTS idx_sessions_expiry
ON auth_sessions(expires_at);

CREATE INDEX IF NOT EXISTS idx_users_role
ON users(role);
