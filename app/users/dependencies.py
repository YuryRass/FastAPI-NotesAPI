"""
Зависимости, которые применяются к пользователям,
заходящим на сайт 'BookingHotels'
"""

from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import get_settings
from app.exceptions import (
    IncorrectJWTtokenException,
    JWTtokenExpiredException,
    UserIsNotPresentException,
    UserUnauthorizedException,
)
from app.users.dao import UsersDAO
from app.users.model import Users

settings = get_settings()


def get_token(request: Request) -> str | None:
    """Возвращает токен пользователя по его HTTP запросу."""
    token: str | None = request.cookies.get(settings.COOKIE_KEY)
    if not token:
        raise UserUnauthorizedException
    return token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    """Возвращает пользователя по его JWT токену

    Args:
        token (str, optional): токен. Defaults to Depends(get_token).

    Raises:
        HTTPException: IncorrectJWTtokenException
        HTTPException: JWTtokenExpiredException
        HTTPException: UserIsNotPresentException

    Returns:
        Users: пользователь
    """
    try:
        payload: dict[str, str] = jwt.decode(
            token=token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectJWTtokenException

    expire: str | None = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now().timestamp()):
        raise JWTtokenExpiredException

    user_id: str | None = payload.get("sub")
    if user_id:
        user: Users = await UsersDAO.find_one_or_none(id=int(user_id))
        if user:
            return user
    raise UserIsNotPresentException
