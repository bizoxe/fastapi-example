from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from core.models.base import Base, engine
from app.posts.views import posts_router
from app.users import users_router
from login_view import log_user
from auth import auth_router
from app.users.votes_view import votes_router
from core.config import settings

# Base.metadata.create_all(engine)
# origins = ["https://www.google.com"]
origins = [
    "*"
]  # разрешить доступ из всех доменов, хорошей практикой является определять список доменов, с которых можно делать запрос к API
app = FastAPI()

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(log_user)
app.include_router(votes_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main2:app", reload=True)
