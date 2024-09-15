from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
import psycopg2
from psycopg2.extras import RealDictCursor

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True


SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/testing"
)


engine = create_engine(
    url=str(settings.db.url),
    echo=True,
    echo_pool=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# можно использовать psycopg2 отдельно от sqlalchemy
# это соединение проще прописываем, автоматически rollback, commit excepions,
# только отдельно закрываем соединение, за кадром это все сделано
# connection = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/testing")
# with connection:
#     with connection.cursor() as cur:
#         cur.execute()
#
# connection.close()

############################################################################3

# while True:
#     try:
#         conn = psycopg2.connect(
#             "postgresql://postgres:postgres@localhost:5432/testing",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("DataBase connection successfully!")
#         break
#     except Exception as err:
#         print(err)
