from passlib.context import CryptContext
from pydantic import PostgresDsn, SecretStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

__all__ = [
    "settings",
    "engine",
    "session_maker",
    "pwd_context"
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")

    POSTGRES_URL: PostgresDsn
    JWT_ACCESS_SECRET_KEY: SecretStr
    JWT_REFRESH_SECRET_KEY: SecretStr
    JWT_ACCESS_ALGORITHM: str
    JWT_REFRESH_ALGORITHM: str
    JWT_ACCESS_EXP: PositiveInt
    JWT_REFRESH_EXP: PositiveInt
    TOKEN_TYPE: str
    OAUTH_CLIENT_ID: SecretStr
    OAUTH_CLIENT_SECRET: SecretStr


settings = Settings()
engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
session_maker = async_sessionmaker(bind=engine)
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
