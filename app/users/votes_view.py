from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.auth2.access_token import get_current_user
from app.users.schemas import Vote as PydanticVote
from core.models.base import get_db
from app.posts.models import Vote as TableVote
from app.posts.models import Post

votes_router = APIRouter(
    prefix="/votes",
    tags=["Vote"],
)


@votes_router.post("", status_code=status.HTTP_201_CREATED)
def vote(
    vote: PydanticVote,
    session: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """удаляем или лайкаем пост -> Vote.dir - 0 del/ 1 create"""
    stmt = select(Post).where(Post.id == vote.post_id)
    post_query = session.scalars(stmt).first()
    if not post_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post {vote.post_id} does not exists!",
        )
    stmt = select(TableVote).where(
        TableVote.post_id == vote.post_id, TableVote.user_id == current_user.id
    )
    found_vote = session.scalars(stmt).first()
    if vote.dir == 1:
        # проверяем в бд если такой пост есть, то его уже лайкали, вызываем исключение
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = TableVote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        session.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exists!",
            )
        session.delete(found_vote)
        session.commit()
    return {"message": "vote wos deleted"}
