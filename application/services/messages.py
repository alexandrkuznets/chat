from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from models.message import Message
from schemas.message import MessageResponse


async def get_messages_from_db(
        user_id: int,
        limit: int,
        session: AsyncSession,
) -> List[MessageResponse]:
    try:
        query = select(Message).where(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)).order_by(Message.date).limit(limit)
        result = await session.execute(query)
        return result.scalars()
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))

async def save_message_in_db(sender: int, receiver: int, message: str, session: AsyncSession):
    try:
        message = Message(sender_id=sender, receiver_id=receiver, text=message)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
    except Exception as ex:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(ex))
