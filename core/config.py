from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False


class JWT(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    db: DataBaseConfig
    jwt: JWT  # не вызываем класс т к нет значений по умолчанию -> берем из env


settings = Settings()
print(str(settings.db.url))
print(settings.jwt.secret_key)
print(settings.jwt.algorithm)
# print(settings.db.echo_pool)
