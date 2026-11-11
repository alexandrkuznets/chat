from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dependiences.auth import get_current_user
from application.models.user import User
from application.models.db_common import db_common
from application.schemas.chat import ChatCreateSchema
from application.services.chat import save_chat_in_db

router = APIRouter(prefix="/chats", tags=["chat"])


@router.post("/")
async def create_chat(
    chat: ChatCreateSchema,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(db_common.session_getter)
):
    result = await save_chat_in_db(user_id=current_user.id, companion_id=chat.companion_id, session=session)
    return {"chat_id": result}
