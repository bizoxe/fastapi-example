from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session


from app.users.schemas import UserCreate, UserOut
from core.models.base import get_db
from app.posts.models import User
from app.utils.psw_hashing import hash_pwd


users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@users_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    print(repr(body.password))
    password_hash = hash_pwd(body.password)
    body.password = password_hash
    user = User(**body.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@users_router.get("/{id}", response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.id == id).first()
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist!"
        )
    return user_id
