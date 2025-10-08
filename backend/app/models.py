from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    TIMESTAMP, Text, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from database import Base  # your SQLAlchemy Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    password = relationship("UserPassword", back_populates="user", uselist=False)
    otps = relationship("UserOTP", back_populates="user")


class UserPassword(Base):
    __tablename__ = "user_passwords"
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    password_hash = Column(Text, nullable=False)
    last_changed = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="password")


class UserOTP(Base):
    __tablename__ = "user_otps"
    otp_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    otp_code = Column(String, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="otps")


class UserSession(Base):
    __tablename__ = "user_sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    token = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False)
