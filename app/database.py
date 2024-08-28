from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import get_settings

settings = get_settings()

async_engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)

async_session: async_sessionmaker = async_sessionmaker(
    async_engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Базовый класс для декларативных определений классов."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)
