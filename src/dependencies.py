from annotated_types import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import session_maker

__all__ = [
    "DBSession"
]


async def create_db_session():
    session = session_maker()
    try:
        yield session
    finally:
        await session.aclose()


DBSession = Annotated[AsyncSession, Depends(dependency=create_db_session)]
