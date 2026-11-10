from fastapi import APIRouter

from application.api.auth import router as auth_router
from application.api.messages import router as messages_router
from application.api.chat import router as chat_router
from application.api.websocket import router as ws_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(messages_router)
router.include_router(ws_router)
router.include_router(chat_router)