from app.config import get_settings
from app.notes.dao import NotesDAO
from app.notes.model import Notes
from app.notes.shemas import SNote, SNoteCreate
from app.users.model import Users

settings = get_settings()


class NotesService:
    """Сервисный слой заметок."""

    @classmethod
    async def get_notes(cls, user: Users) -> list[SNote]:
        """Возвращает содержимое всех заметок для конкретного пользователя."""
        return await NotesDAO.find(user_id=user.id)

    @classmethod
    async def add_note_for_user(
        cls,
        note: SNoteCreate,
        user: Users,
    ) -> SNote:
        """Добавляет заметку."""

        note: Notes | None = await NotesDAO.add(user_id=user.id, content=note.content)
        return note
