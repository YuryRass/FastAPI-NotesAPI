from fastapi import APIRouter, Depends, Response

from app.config import get_settings
from app.exceptions import IncorrectEmailOrPasswordException, UserIsAllredyRegistered
from app.users.auth import authentication_user, create_jwt_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.model import Users
from app.users.service import UserService
from app.users.shemas import SUserAuth, SUserOut

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["Auth & users"],
)

settings = get_settings()


@router.post("/register", summary="Регистрация пользователя")
async def user_register(user_data: SUserAuth) -> None:
    """Регистрация пользователя."""
    return await UserService.user_register(user_data)


@router.post("/login", summary="Вход на сайт")
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    """Вход пользователя на сайт."""
    return await UserService.login_user(response, user_data)


@router.post("/logout", summary="Выход из сайта")
async def logout_user(response: Response) -> None:
    """Выход пользователя из сайта."""
    return await UserService.logout_user(response)


@router.get("/me", summary="Информация о пользователе")
async def read_users_me(current_user: Users = Depends(get_current_user)) -> SUserOut:
    """Вывод инфорации (e-mail) о текущем пользователе."""
    return await UserService.read_users_me(current_user)
