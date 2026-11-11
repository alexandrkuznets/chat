from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.exception.chat import ChatBadRequest
from application.exception.messages import ConversationNotFound
from application.models.user import User
from application.models.chat import Chat, ChatParticipant


async def save_chat_in_db(user_id: int, companion_id:int, session: AsyncSession):
    if user_id == companion_id:
        raise ChatBadRequest
    try:
        query = select(User).where(User.id == companion_id)
        result = await session.execute(query)
        companion = result.scalar_one_or_none()

        if companion is None:
            raise ConversationNotFound

        query = (select(
            ChatParticipant.chat_id).
                 where(ChatParticipant.user_id.in_([user_id, companion_id])).
                 group_by(ChatParticipant.chat_id).
                 having(func.count(ChatParticipant.user_id) == 2)
                 )
        result = await session.execute(query)
        chat_participant = result.scalar_one_or_none()
        if chat_participant:

            return chat_participant

        chat = Chat()
        session.add(chat)
        await session.flush()

        user = ChatParticipant(chat_id=chat.id, user_id=user_id)
        companion = ChatParticipant(chat_id=chat.id, user_id=companion_id)
        session.add(user)
        session.add(companion)

        await session.commit()
        return chat.id
    except SQLAlchemyError as e:
        await session.rollback()
        raise


