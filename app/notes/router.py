"""Конечные точки для бронирования отелей"""

from fastapi import APIRouter, Depends

from app.notes.service import NotesService
from app.notes.shemas import SNote, SNoteCreate
from app.users.dependencies import get_current_user
from app.users.model import Users

router: APIRouter = APIRouter(prefix="/notes", tags=["Заметки пользователей"])


@router.get("", summary="Список всех заметок")
async def get_notes(user: Users = Depends(get_current_user)) -> list[SNote]:
    """Возвращает содержимое всех заметок для конкретного пользователя."""
    return await NotesService.get_notes(user)


@router.post("", summary="Добавление заметки")
async def add_note_for_user(
    note: SNoteCreate,
    user: Users = Depends(get_current_user),
) -> SNote:
    """Добавляет заметку для авторизованного пользователя."""

    return await NotesService.add_note_for_user(note, user)
