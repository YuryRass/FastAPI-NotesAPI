"""Модель пользователей"""
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.notes.model import Notes


class Users(Base):
    """Пользователи."""

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    notes: Mapped[list["Notes"]] = relationship(back_populates="user")

    def __str__(self) -> str:
        return f"User: {self.email}"