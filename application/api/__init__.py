from fastapi import APIRouter

from .auth import router as auth_router
from .messages import router as messages_router
from .websocket import router as ws_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(messages_router)
router.include_router(ws_router)