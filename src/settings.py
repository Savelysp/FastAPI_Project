from passlib.context import CryptContext
from pydantic import PostgresDsn, SecretStr, PositiveInt, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


__all__ = [
    "settings",
    "engine",
    "session_maker",
    "pwd_context",
    "bot",
    "dp"
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

    TELEGRAM_BOT_TOKEN: SecretStr
    TELEGRAM_SECRET_TOKEN: SecretStr

    DOMAIN: AnyUrl


settings = Settings()
engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
session_maker = async_sessionmaker(bind=engine)
pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
    parse_mode=ParseMode.HTML
)
dp = Dispatcher()

