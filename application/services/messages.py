from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

from models.message import Message
from models.user import User
from schemas.message import MessageResponse
from exception.messages import ConversationNotFound


async def get_messages_from_db(
        user_id: int,
        current_user_id: int,
        offset: int,
        limit: int,
        session: AsyncSession,
) -> List[MessageResponse]:
    stmt_1 = and_(Message.sender_id == user_id, Message.receiver_id == current_user_id)
    stmt_2 = and_(Message.sender_id == current_user_id, Message.receiver_id == user_id)
    query = select(Message).where(
        or_(stmt_1, stmt_2)).order_by(Message.date).offset(offset).limit(limit)
    try:
        result = await session.execute(query)
        return list(result.scalars().all())
    except Exception as ex:
        raise ex


async def save_message_in_db(sender: int, receiver: int, text: str, session: AsyncSession):
    query = select(User).where(User.id == receiver)
    result = await session.execute(query)
    if result.scalar_one_or_none() is None:
        raise ConversationNotFound
    try:
        message = Message(sender_id=sender, receiver_id=receiver, text=text)
        session.add(message)
        await session.commit()
        await session.refresh(message)
        return message
    except Exception as ex:
        await session.rollback()
        raise ex
