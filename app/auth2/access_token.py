from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.posts.models import User
from app.users.schemas import TokenData
from core.models.base import get_db
from core.config import settings

# эти данные ключ алгоритм минуты -> env
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth2_scheme = OAuth2PasswordBearer(tokenUrl="login2")


def create_access_token(data: dict):
    """Create JWT."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt.access_token_expire_minutes
    )
    # в payload ключи claims рекомендованные -> exp зарезервированный клэйм
    # отсебятину здесь время истечения не можем передавать
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    try:
        pyload = jwt.decode(
            jwt=token,
            key=SECRET_KEY,
            algorithms=ALGORITHM,
        )
        user_id: int = pyload.get("user_id")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(id=user_id)
    except jwt.exceptions.PyJWTError:
        raise credential_exception

    return token_data


def get_current_user(
    token: str = Depends(auth2_scheme), session: Session = Depends(get_db)
):
    """Разбили на две функции т. как здесь в get_current_user получаем нашего пользователя и в дальнейшем можем с ним что то делать"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credential_exception)
    stmt = select(User).where(User.id == token.id)
    user = session.scalars(stmt).first()
    return user
