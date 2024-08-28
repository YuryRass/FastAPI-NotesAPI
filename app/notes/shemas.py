from typing import Any

import httpx
from pydantic import BaseModel, field_validator

from app.config import get_settings

settings = get_settings()


class SpellerService:
    @staticmethod
    def check_spelling(text: str) -> Any:
        """Проверка текста на орфографические ошибки."""
        params = {"text": text}
        response = httpx.get(settings.SPELLER_URL, params=params)

        if response.status_code != 200:
            raise Exception("Error connecting to Yandex.Speller")

        return response.json()


class SNote(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


class SNoteCreate(BaseModel):
    content: str

    @field_validator("content")
    def validate_content(cls, value: str) -> str:
        """Проверяет текст с помощью Яндекс.Спеллера."""

        mistakes = SpellerService.check_spelling(value)
        if mistakes:
            error_messages = [
                f"{mistake['s'][0]} in the word '{mistake['word']}'"
                for mistake in mistakes
            ]
            raise ValueError("; ".join(error_messages))
        return value
