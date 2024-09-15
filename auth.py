from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.posts.models import User

from app.users.schemas import UserLogin, Token
from app.utils.psw_hashing import check_pwd
from core.models.base import get_db
from app.auth22 import create_access_token

auth_router = APIRouter(
    tags=["Authentication"],
)


# auth_roter = APIRouter(
#     tags=["Authentication"],
# )
#
#
# @auth_roter.post("/login")
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
#
#
#     user = db.query(User).filter(User.email == user_credentials.email).first()
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!"
#         )
#     print(user.password)
#     valid_pwd = check_pwd(user_credentials.password, user.password)
#     if not valid_pwd:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password!"
#         )
#     # create a token
#     token = create_access_token(data={"user_id": user.id})
#     return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # user = db.query(User).filter(User.email == user_credentials.email).first()
    stmt = select(User).where(User.email == user_credentials.username)
    user = db.scalars(stmt).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"email {user_credentials.username} does not exist!",
        )
    is_valid = check_pwd(user_credentials.password, user.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"password ({user_credentials.password}) does not exist or incorrect!",
        )
    # create token
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
