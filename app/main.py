from fastapi import FastAPI


from app.users.router import router as user_router
from app.notes.router import router as note_router

app: FastAPI = FastAPI()

app.include_router(user_router)
app.include_router(note_router)