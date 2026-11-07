from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dependiences.auth import get_current_user
from application.models.db_common import db_common
from application.models.user import User
from application.services.websocket import manager

router = APIRouter(prefix="/ws")


@router.websocket("{room_id}/")
async def send_messages(
        room_id: int,
        websocket: WebSocket,
        session: AsyncSession = Depends(db_common.session_getter),
        current_user: User = Depends(get_current_user),
):
    await manager.connect(websocket=websocket, room_id=room_id, user_id=current_user.id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{current_user.username}: {data}", room_id=room_id, sender_id=current_user.id)
    except WebSocketDisconnect:
        await manager.disconnect(room_id=room_id, user_id=current_user.id)
