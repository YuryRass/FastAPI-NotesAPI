"""Реализация модели 'Заметки"""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.users.model import Users


class Notes(Base):
    """Заметки пользователей."""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str]

    user: Mapped["Users"] = relationship(back_populates="notes")

    def __str__(self) -> str:
        return f"Note #{self.id}"