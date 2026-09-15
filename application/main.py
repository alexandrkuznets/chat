import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router as chat_router
from core.config import settings
from models.db_common import db_common
from exception.base import BaseAPIException
from exception.exception_handler import handle_api_exceptions


async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_common.dispose()


app = FastAPI(
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_exception_handler(BaseAPIException, handle_api_exceptions)
app.include_router(
    chat_router,
    prefix=settings.api.prefix,
)

if __name__ == "__main__":
    uvicorn.run("main:app",
                port=settings.run.port,
                host=settings.run.host,
                reload=True
                )
