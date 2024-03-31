from datetime import datetime, timedelta, UTC

from jwt import encode, decode
from jwt.exceptions import PyJWTError, InvalidTokenError, ExpiredSignatureError

from src.settings import settings

__all__ = [
    "create_access_token",
    "create_refresh_token",
    "verify_access_token",
    "verify_refresh_token"
]


def create_jwt(*, payload: dict, exp: int, key: str, algorithm: str) -> str:
    if "sub" not in payload:
        raise AttributeError

    payload["exp"] = datetime.now(tz=UTC) + timedelta(minutes=exp)
    return encode(payload=payload, key=key, algorithm=algorithm)


def verify_jwt(*, jwt: str, key: str, algorithm: str) -> dict:
    try:
        return decode(
            jwt=jwt,
            key=key,
            algorithms=[algorithm]
        )
    except ExpiredSignatureError:
        raise ValueError("Token expired")
    except InvalidTokenError:
        raise ValueError("Invalid token")
    except PyJWTError:
        raise ValueError("Incorrect token")


def create_access_token(payload: dict) -> str:
    return create_jwt(
        payload=payload,
        exp=settings.JWT_ACCESS_EXP,
        algorithm=settings.JWT_ACCESS_ALGORITHM,
        key=settings.JWT_ACCESS_SECRET_KEY.get_secret_value()
    )


def create_refresh_token(payload: dict) -> str:
    return create_jwt(
        payload=payload,
        exp=settings.JWT_REFRESH_EXP,
        algorithm=settings.JWT_REFRESH_ALGORITHM,
        key=settings.JWT_REFRESH_SECRET_KEY.get_secret_value()
    )


def verify_access_token(jwt: str) -> dict:
    return verify_jwt(
        jwt=jwt,
        algorithm=settings.JWT_ACCESS_ALGORITHM,
        key=settings.JWT_ACCESS_SECRET_KEY.get_secret_value()
    )


def verify_refresh_token(jwt: str) -> dict:
    return verify_jwt(
        jwt=jwt,
        algorithm=settings.JWT_REFRESH_ALGORITHM,
        key=settings.JWT_REFRESH_SECRET_KEY.get_secret_value()
    )
