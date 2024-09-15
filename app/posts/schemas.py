from datetime import datetime

from typing import Optional, Dict

from pydantic import BaseModel, ConfigDict

from app.users.schemas import UserOut


# ГРАМОТНО наследуемся при создании СХЕМ смотри код внизу закоментированный
# при создании и обновлении модели как правило одинаковы()
# то есть UpdatePost можно не создавать(если не стоит задача обновлять определенные поля)
# то есть не все поля, которые определялись при создании объекта
class PostBase(BaseModel):
    title: str
    content: str
    published: bool | None = True
    # published: Union[bool, None] = True
    rating: Optional[int] = 0


class CreatePost(PostBase):
    pass


# можем не дублировать код, наследоваться от базового класса, просто добавив нужные поля
class PostResponse(PostBase):
    id: int
    user_id: int
    owner: UserOut
    created_at: datetime  # так можно передать объект даты из бд
    updated_at: datetime
    # class Config: -> устарело, сам pydantic работает со словарями, если возвращаем, например объект ORM, происходила бы ошибка
    #     orm_mod = True
    model_config = (
        ConfigDict(  # -> уже является по умолчанию и необязательно явно прописывать
            from_attributes=True,
        )
    )  # т.е извлекает значения из аттрибутов -> для ORM


class PostResponseVote(BaseModel):
    Post: PostResponse
    votes_count: int
    model_config = ConfigDict(from_attributes=True)


# отнаследовался от PostBase, PostResponse уже наследник PostBase
# произошел конфликт полей!!!!!!
# class PostResponseVote(PostBase):
#     Post: PostResponse
#     votes_count: int
#     model_config = ConfigDict(from_attributes=True)
