from random import randrange
from typing import Union, Optional


from fastapi import FastAPI
from fastapi import Body
from fastapi import Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool | None = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "title of post 2",
        "content": "content of post 2",
        "id": 2,
    },
]


# connection to database


def get_post_from_list(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return


def find_post_by_id(id):
    print(id)
    for index, element in enumerate(my_posts):
        if element["id"] == id:
            return index
    return


def find_index(id: int, lst: list):
    for index, element in enumerate(lst):
        if element["id"] == id:
            return index
    return None


@app.get("/")
def root():
    return {"message": "success"}


@app.get("/posts/latest")
def get_post_latest():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    """get post by id"""
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id {id} does not exist!",
        )

    # post = get_post_from_list(id)
    # if not post:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"post with id {id} was not found!",
    #     )
    return {"message": result}


@app.get("/posts")
def get_posts():
    """get all posts"""
    cursor.execute("""SELECT * FROM posts;""")
    result = cursor.fetchall()
    print(result)
    return {"data": result}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS posts 
                    (id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
                    title VARCHAR NOT NULL,
                    content VARCHAR NOT NULL,
                    published BOOLEAN DEFAULT True,
                    rating INTEGER DEFAULT 0);"""
    )
    cursor.execute(
        """INSERT INTO posts (title, content, published, rating)
                    VALUES (%s, %s, %s, %s)""",
        (
            new_post.title,
            new_post.content,
            new_post.published,
            new_post.rating,
        ),
    )
    conn.commit()
    result = cursor.rowcount

    return {"data": new_post, "result": result}  # вернем пользователю созданный объект


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """ "Delete post обязательно обрабатываем не сущестующий id"""
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} does not exists!"
        )

    # index = find_post_by_id(id)
    # if index is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found!"
    #     )
    # else:
    #     my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """Update post"""
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    result = cursor.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"id {id} does not exist!",
        )

    cursor.execute(
        """UPDATE posts SET title = %s, content = %s,
                published = %s, rating = %s WHERE id = %s RETURNING *""",
        (
            post.title,
            post.content,
            post.published,
            post.rating,
            id,
        ),
    )
    conn.commit()
    result = cursor.fetchone()

    return {"message": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
