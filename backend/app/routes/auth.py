from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

from models import User, UserPassword, UserOTP, UserSession
from schemas import RegisterRequest, LoginRequest, OTPVerifyRequest
from utils import hash_password, verify_password, generate_otp, otp_expiry
from database import get_db

SECRET_KEY = "supersecret"
router = APIRouter(prefix="/auth", tags=["Auth"])

# REGISTER
@router.post("/register")
def register_user(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(email=req.email, phone=req.phone)
    db.add(user)
    db.commit()
    db.refresh(user)

    # If password provided, store it
    if req.password:
        hashed = hash_password(req.password)
        db.add(UserPassword(user_id=user.user_id, password_hash=hashed))
        db.commit()

    # Generate OTP for verification
    otp_code = generate_otp()
    db.add(UserOTP(user_id=user.user_id, otp_code=otp_code, expires_at=otp_expiry()))
    db.commit()

    # In real system, send via email or SMS
    return {"message": "User registered. OTP sent.", "otp_demo": otp_code}


# LOGIN (password or OTP)
@router.post("/login")
def login_user(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if req.password:
        pw = db.query(UserPassword).filter(UserPassword.user_id == user.user_id).first()
        if not pw or not verify_password(req.password, pw.password_hash):
            raise HTTPException(status_code=401, detail="Invalid password")
    else:
        otp_code = generate_otp()
        db.add(UserOTP(user_id=user.user_id, otp_code=otp_code, expires_at=otp_expiry()))
        db.commit()
        return {"message": "OTP sent for login", "otp_demo": otp_code}

    # Issue session token
    token = jwt.encode(
        {"user_id": user.user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    session = UserSession(
        user_id=user.user_id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(session)
    db.commit()

    return {"access_token": token, "token_type": "bearer"}


# VERIFY OTP
@router.post("/verify-otp")
def verify_otp(req: OTPVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_entry = (
        db.query(UserOTP)
        .filter(
            UserOTP.user_id == user.user_id,
            UserOTP.otp_code == req.otp,
            UserOTP.expires_at > datetime.utcnow(),
            UserOTP.is_used == False
        )
        .first()
    )

    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    otp_entry.is_used = True
    user.is_verified = True
    db.commit()

    # Issue JWT
    token = jwt.encode(
        {"user_id": user.user_id, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )

    session = UserSession(
        user_id=user.user_id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(session)
    db.commit()

    return {"access_token": token, "token_type": "bearer"}
