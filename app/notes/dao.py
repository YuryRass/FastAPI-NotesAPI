"""Класс, реализующий CRUD-операции к модели 'Заметки'"""

from app.dao.base import BaseDAO
from app.notes.model import Notes


class NotesDAO(BaseDAO):
    """DAO объект 'Заметки'"""

    model = Notes
