from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependiences.auth import get_current_user
from models.db_common import db_common
from models.user import User
from schemas.message import MessageResponse
from services.messages import get_messages_from_db

router = APIRouter(prefix="/conversation", tags=["messages"])


@router.get("/{user_id}/messages/")
async def get_messages(
        user_id: int,
        limit: int = 50,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_common.session_getter)
) -> List[MessageResponse]:
    result = await get_messages_from_db(user_id, limit, session)
    return result
