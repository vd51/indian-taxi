from pydantic import BaseModel, Field
from typing import Optional
class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=80)
    phone: str = Field(min_length=10, max_length=13)
    email: Optional[str] = None
    password: str = Field(min_length=8, max_length=128)
class OTPVerifyRequest(BaseModel):
    challenge_id: str
    phone: str
    otp: str = Field(min_length=6, max_length=6)
class LoginRequest(BaseModel):
    phone: str
    password: str
