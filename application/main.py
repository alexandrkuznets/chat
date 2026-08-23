import uvicorn
from fastapi import FastAPI

from api import router as chat_router
from core.config import settings

app = FastAPI()
app.include_router(
    chat_router,
    prefix=settings.api.prefix,
)

if __name__=="__main__":
    uvicorn.run("main:app",
                port=settings.run.port,
                host=settings.run.host,
                reload=True
    )
