import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Depends, HTTPException

from typing import Annotated

from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from models.db_common import db_common
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user(username: str, session: AsyncSession):
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(db_common.session_getter)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key.get_secret_value(), algorithms=[settings.algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(username, session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(db_common.session_getter)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
