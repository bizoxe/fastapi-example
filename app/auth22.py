# use pyjwt
# we need
# SECRET KEY
# Algorithm
# Expiration time (время истечения токена) иначе юзер будет вечно в состоянии log in
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.posts.models import User
from app.users.schemas import TokenData
from core.models.base import get_db

# import jwt -> из установленного pyjwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    """Create access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        pyload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: int = pyload.get("user_id")
        print(type(id))
        if id is None:
            raise credentials_exception

        token_data = TokenData(id=id)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(auth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    stmt = select(User).where(User.id == token.id)
    user = db.scalars(stmt).first()

    return user
