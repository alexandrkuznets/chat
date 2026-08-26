from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))