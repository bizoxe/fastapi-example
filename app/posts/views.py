from typing import List, Optional, Dict

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy import select, func, label
from sqlalchemy.orm import Session

from app.auth2.access_token import get_current_user
from app.posts.schemas import CreatePost, PostResponse, PostResponseVote
from core.models.base import get_db
from app.posts.models import Post, Vote

posts_router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# @posts_router.get("", response_model=List[PostResponse])
@posts_router.get(
    "", response_model=List[PostResponseVote]
)  # здесь мы отдаем список объектов из БД!!!-> List
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 5,
    skip: int = 0,
    search: Optional[str] = "",
):
    """get all posts for an authorized user"""
    # stmt = select(Post).filter(Post.title.contains(search)).limit(limit).offset(skip)
    # stmt = select(Post).where(Post.user_id == current_user.id).limit(limit).offset(skip)
    stmt2 = (
        select(Post, label("votes_count", func.count(Vote.post_id)))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .where(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
    )

    # fetchmany() - > limit
    # posts = db.scalars(stmt).all()
    # stmt = select(Post).filter(Post.user_id == current_user.id)
    posts = db.execute(stmt2).mappings().all()

    # posts2 = (
    #     db.query(Post, func.count(Vote.post_id).label("vote"))
    #     .join(Vote, Post.id == Vote.post_id, isouter=True)
    #     .group_by(Post.id)
    # ).all() #- DEPRECATED
    # print(posts2)
    # posts = db.query(Post).all() #- DEPRECATED

    return posts  # не обязательно отдавать -> {}, отдаем просто объект, фастапи сериализует его сам

    # all_posts = db.query(Post).all()
    # print(all_posts, "all posts")
    # return {"data": all_posts}


@posts_router.post("", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    body: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """create post проверяем на аутентификацию -> user_id: int = Depends(get_current_user)"""
    # post = Post(
    #     title=body.title,
    #     content=body.content,
    #     published=body.published,
    #     rating=body.rating,
    # )
    post = Post(user_id=current_user.id, **body.model_dump())
    # поле из 'posts' user_id -> NOT NULL -> на фронте мы его не ожидаем -> CreatePost этого поля нет
    # поэтому забираем из current_user
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


# @posts_router.get("/{id}", response_model=PostResponse)
@posts_router.get("/{id}", response_model=PostResponseVote)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """get post by id + votes"""
    # post_id = db.query(Post).filter(Post.id == id).first()
    stmt = (
        select(Post, func.count(Vote.post_id).label("votes_count"))
        .join(Vote, Vote.user_id == Post.id, isouter=True)
        .group_by(Post.id)
        .where(Post.id == id)
    )
    print(stmt)
    post_id = db.execute(stmt).mappings().one_or_none()
    print(post_id)
    if post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id ({id}) does not exist!",
        )
    return post_id


@posts_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    """delete post by id"""
    query_post = db.query(Post).filter(Post.id == id)
    post = query_post.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist!"
        )
    # аналогично db.query(Post).filter(Post.id == id).delete()
    # post = db.query(Post).filter(Post.id == id).delete()
    # здесь проверяем является ли пользователь владельцем поста
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    query_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@posts_router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int,
    body: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exist!"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.update(body.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post_query.first()
