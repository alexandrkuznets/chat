from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.auth import authenticate_user, create_access_token
from core.config import settings
from dependiences.auth import get_current_active_user
from models.user import User
from models.db_common import db_common
from schemas.token import Token
from schemas.user import UserResponse, UserCreate
from services.user import create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(db_common.session_getter)
) -> Token:
    # logger.info(f"Попытка логина: пользователь {form_data.username}")
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        # logger.warning(f"Неудачный логин: пользователь {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=settings.auth.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    # logger.info(f"Создан JWT токен: пользователь {form_data.username}")
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register/")
async def register(
        user: UserCreate,
        session: AsyncSession = Depends(db_common.session_getter)
) -> UserResponse:
    result = await create_user(user, session)
    return result


@router.get("/users/me/")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)],
        session: AsyncSession = Depends(db_common.session_getter)
) -> UserResponse:
    # logger.info(f"Запрос /users/me: user_id={current_user.id}")
    # logger.info(f"Профиль получен: user_id={current_user.id}")
    return current_user
