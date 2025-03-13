import os
from os import path
from typing import Annotated, Literal, List

from fastapi import Depends
from pydantic import BaseModel, Json, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode

__all__ = (
    'get_settings',
    'Settings',
    'settings',
)


class Db(BaseModel):
    """
    Настройки для подключения к базе данных.
    """

    host: str
    port: int
    user: str
    password: str
    name: str
    scheme: str = 'public'

    provider: str = 'postgresql+psycopg_async'

    @property
    def dsn(self) -> str:
        return f'{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class S3(BaseModel):
    """
    Настройки для S3.
    """

    endpoint: str
    access_key: str
    secret_key: str
    port: int
    bucket: str
    secure: bool = False


class Storage(BaseModel):
    """
    Настройки для хранилища.
    """

    provider: Literal['local', 's3'] = 'local'

    dir: str | None = path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage')
    s3: S3 | None = None


class Cache(BaseModel):
    """
    Настройки кеша.
    """

    prefix: str = 'boiler-plate'


class JWT(BaseModel):
    """
    Настройки JWT токена.
    """

    token_algorithm: str


class AccessToken(BaseModel):
    """
    Настройки Access JWT токена.
    """
    token_lifetime_minutes: int


class RefreshToken(BaseModel):
    """
    Настройки Refresh токена.
    """
    token_lifetime_days: int

class JWTCookie(BaseModel):
    """
    Настройки создания куки с JWT токеном.
    """

    token_lifetime: int
    cookie_name: str
    cookie_max_age: int
    cookie_path: str
    cookie_secure: bool
    cookie_samesite: Literal['lax', 'strict', 'none']


class Settings(BaseSettings):
    """
    Настройки модели.
    """

    debug: bool
    base_url: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    secret_key: str
    cors_origins: Annotated[List[str], NoDecode] 
    

    @field_validator('cors_origins', mode='before')
    @classmethod
    def decode_cors_origins(cls, v: str) -> List[str]:
        return [x for x in v.split(',')]

    db: Db
    #storage: Storage
    #cache: Cache

    jwt: JWT
    access_token: AccessToken
    refresh_token: RefreshToken
    #jwt_cookie: JWTCookie

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
        case_sensitive=False,
        extra='ignore',
        env_prefix='SCHOOL_SITE_APP_',
    )


def get_settings():
    return Settings()  # type: ignore


settings = get_settings()

SettingsService = Annotated[Settings, Depends(get_settings)]