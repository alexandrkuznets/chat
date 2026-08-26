from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Message(Base):
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str]
    date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
