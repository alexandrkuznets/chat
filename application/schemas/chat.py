from pydantic import BaseModel


class ChatCreateSchema(BaseModel):
    companion_id: int

