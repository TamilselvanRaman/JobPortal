import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Tuple

from jose import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
	return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
	return hash_password(plain) == hashed


def create_access_token(data: dict) -> Tuple[str, int]:
	"""Create JWT access token. Returns (token, expires_at_seconds)"""
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
	return token, int(expire.timestamp())


def create_refresh_token() -> str:
	return uuid.uuid4().hex
