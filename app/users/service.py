from fastapi import Depends, Response

from app.config import get_settings
from app.exceptions import IncorrectEmailOrPasswordException, UserIsAllredyRegistered
from app.users.auth import authentication_user, create_jwt_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.model import Users
from app.users.shemas import SUserAuth, SUserOut


settings = get_settings()


class UserService:
    """Сервисный слой пользователя."""

    @classmethod
    async def user_register(cls, user_data: SUserAuth) -> None:
        """Регистрация пользователя."""
        existing_user: Users | None = await UsersDAO.find_one_or_none(
            email=user_data.email
        )
        # Если пользователь уже есть в БД (т.е. он зарегитсрирован),
        # то мы вызываем исключение (повторная регистрация нам не нужна)
        if existing_user:
            raise UserIsAllredyRegistered
        password_hash: str = get_password_hash(password=user_data.password)
        await UsersDAO.add(email=user_data.email, hashed_password=password_hash)

    @classmethod
    async def login_user(cls, response: Response, user_data: SUserAuth) -> dict:
        """Вход пользователя на сайт."""
        user: Users | None = await authentication_user(
            user_data.email, user_data.password
        )
        if not user:
            raise IncorrectEmailOrPasswordException
        else:
            jwt_token: str = create_jwt_token({"sub": str(user.id)})
            response.set_cookie(key=settings.COOKIE_KEY, value=jwt_token, httponly=True)
            return {"JWT token": jwt_token}

    @classmethod
    async def logout_user(cls, response: Response) -> None:
        """Выход пользователя из сайта."""
        response.delete_cookie(key=settings.COOKIE_KEY)

    @classmethod
    async def read_users_me(cls, current_user: Users) -> SUserOut:
        """Вывод инфорации (e-mail) о текущем пользователе."""
        return current_user
