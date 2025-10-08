import random, string, bcrypt
from datetime import datetime, timedelta

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def otp_expiry(minutes=5):
    return datetime.utcnow() + timedelta(minutes=minutes)
