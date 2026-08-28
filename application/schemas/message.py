from pydantic import BaseModel
from datetime import datetime

class BaseMessageSchema(BaseModel):
    sender_id: int
    receiver_id: int
    text: str

class MessageCreate(BaseMessageSchema):
    pass

class MessageResponse(BaseMessageSchema):
    date: datetime

