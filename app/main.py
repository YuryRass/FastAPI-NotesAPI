from fastapi import FastAPI

from app.notes.router import router as note_router
from app.users.router import router as user_router

app: FastAPI = FastAPI()


@app.get("/")
def get_app_info() -> dict:
    return {"Веб-приложение на FastAPI": "Заметки пользователей"}


app.include_router(user_router)
app.include_router(note_router)
