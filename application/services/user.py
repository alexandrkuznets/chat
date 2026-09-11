from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.auth import hash_password
from schemas.user import UserCreate, UserResponse
from models.user import User


async def create_user(user: UserCreate, session: AsyncSession) -> UserResponse:
    if user.password1 != user.password2:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    result = await session.execute(select(User).where(User.username == user.username))
    if result.fetchall():
        raise HTTPException(status_code=409, detail="Этот никнейм уже используется")

    password_hashed = hash_password(user.password1)
    try:
        user = User(username=user.username, password=password_hashed)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        # logger.info(f"Пользователь создан: {user.email}")
        return user
    except Exception as ex:
        # logger.error(f"Ошибка создания пользователя! {user.email}. {ex}")
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))
