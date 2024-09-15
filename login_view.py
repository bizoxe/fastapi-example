from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.auth2.access_token import create_access_token
from app.posts.models import User
from app.users.schemas import Token
from app.utils.psw_hashing import check_pwd
from core.models.base import get_db

# для получения username, password используем для пользователя форму из fastapi ->
# -> OAuth2PasswordRequestForm
log_user = APIRouter(
    tags=["Login"],
)


@log_user.post("/login2", response_model=Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    stmt = select(User).where(User.email == user_credentials.username)
    user = session.scalars(stmt).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"email ({user_credentials.username}) does not exists or incorrect!",
        )
    pwd = check_pwd(user_credentials.password, user.password)
    if not pwd:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"password ({user_credentials.password}) is incorrect!",
        )
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
