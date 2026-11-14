from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: list = ["http://127.0.0.1:8001", "http://localhost:8001", "*"]
    SESSION_DAYS: int = 30
    ACCESS_TOKEN_MINUTES: int = 60
    OTP_MINUTES: int = 5
    OTP_MAX_ATTEMPTS: int = 5
    OTP_EXPOSE_IN_DEVELOPMENT: bool = True
    SECRET_KEY: str = "indian-taxi-pro-2026-secret-key-change-in-production"
    DATABASE_PATH: str = "indian_taxi.db"
settings = Settings()
