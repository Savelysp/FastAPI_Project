from datetime import datetime
from time import time
from typing import TYPE_CHECKING

from email_validator import EmailSyntaxError
from sqlalchemy import Column, BIGINT, VARCHAR, CheckConstraint, CHAR, BOOLEAN, ForeignKey, TIMESTAMP, DECIMAL
from sqlalchemy.orm import validates, relationship

from .base import Base

__all__ = [
    "User",
    "Service",
    "Entry",
    "Base"
]


class User(Base):
    __table_args__ = (
        CheckConstraint("length(email) >=5"),
        CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z]{2,}$'"),
    )

    if TYPE_CHECKING:
        id: int
        email: str
        password: str
        is_admin: bool
        entries: list["Entry"]
    else:
        id = Column(BIGINT, primary_key=True)
        email = Column(VARCHAR(length=128), nullable=True, unique=True)
        password = Column(CHAR(length=60), nullable=True)
        is_admin = Column(BOOLEAN, default=False)
        entries = relationship(argument="Entry", back_populates="user")

    def __str__(self) -> str:
        return self.email


class Service(Base):
    __table_args__ = (
        CheckConstraint("price > 0"),
    )

    if TYPE_CHECKING:
        id: int
        name: str
        price: float
        title: str
        # entries: list["Entry"]
    else:
        id = Column(BIGINT, primary_key=True)
        name = Column(VARCHAR(128), nullable=False)
        price = Column(DECIMAL(scale=2), nullable=False)
        title = Column(VARCHAR(256), nullable=False)
        # entries = relationship(argument="Entry", back_populates="service")


class Entry(Base):
    # __table_args__ = (
    #     CheckConstraint("entry_time >= now()"),
    # )

    if TYPE_CHECKING:
        id: int
        user_id: int
        # service_id: int
        entry_time: float
        user: User
        # service: Service
    else:
        id = Column(BIGINT, primary_key=True)
        user_id = Column(
            BIGINT,
            ForeignKey(
                column=User.id, # noqa
                ondelete="CASCADE",
                onupdate="CASCADE"
            ),
            nullable=False
        )
        # service_id = Column(
        #     BIGINT,
        #     ForeignKey(
        #         column=Service.id, # noqa
        #         ondelete="CASCADE",
        #         onupdate="CASCADE"
        #     )
        # )
        entry_time = Column(TIMESTAMP, nullable=False, unique=True)
        user = relationship(argument=User, back_populates="entries")
        # service = relationship(argument=Service, back_populates="entries")
