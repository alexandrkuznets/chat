import jwt
from pwdlib import PasswordHash
from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from application.core.config import settings
from application.dependiences.auth import get_user

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user(username, session)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth.secret_key.get_secret_value(), algorithm=settings.auth.algorithm)
    return encoded_jwt
