from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependiences.auth import get_current_user
from models.db_common import db_common
from models.user import User
from schemas.message import MessageResponse, MessageCreate
from services.messages import get_messages_from_db, save_message_in_db

router = APIRouter(prefix="/conversation", tags=["messages"])


@router.get("/messages/")
async def get_messages(
        limit: int = 50,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_common.session_getter)
) -> List[MessageResponse]:
    result = await get_messages_from_db(current_user.id, limit, session)
    return result


@router.post("/{user_id}/messages/")
async def send_messages(
        user_id: int,
        message: str,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_common.session_getter)
) -> MessageCreate:
    result = await save_message_in_db(receiver=user_id, sender=current_user.id, message=message, session=session)
    return result
