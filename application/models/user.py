from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from datetime import datetime, timezone

from application.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    chat_participant: Mapped[list["ChatParticipant"]] = relationship(
        back_populates="user"
    )
    messages: Mapped[list["Message"]] = relationship(back_populates="sender")