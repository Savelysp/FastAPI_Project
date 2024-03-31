from src.settings import pwd_context

__all__ = [
    "create_password_hash",
    "password_verify"
]


def create_password_hash(password: str) -> str:
    return pwd_context.hash(secret=password)


def password_verify(password: str, password_hash: str) -> bool:
    return pwd_context.verify(secret=password, hash=password_hash)
