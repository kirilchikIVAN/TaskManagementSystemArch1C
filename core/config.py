import typing

from pydantic import BaseSettings, PostgresDsn, validator


class CustomBaseSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = 'utf-8'


class DBSettings(CustomBaseSettings):
    host: str = "localhost"
    username: str = "postgres"
    password: str
    port: str = "5432"
    name: str = "db"
    uri: PostgresDsn

    @validator("uri", pre=True)
    def sqlalchemy_database_uri_init(cls, v: str | None, values: dict[str, typing.Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values["username"],
            password=values["password"],
            host=values["host"],
            port=values["port"],
            path=f"/{values['name'] or ''}",
        )

    class Config(CustomBaseSettings.Config):
        env_prefix = 'db_'


settings_db = DBSettings(uri=None)  # type: ignore
