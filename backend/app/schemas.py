from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = None

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str
