from datetime import datetime

from pydantic import Field, PositiveInt

from .base import Schema

__all__ = [
    "EntryCreateForm",
    "EntryEditForm",
    "EntryDetailForm"
]


class EntryCreateForm(Schema):
    entry_time: datetime = Field(
        default=...,
        title="time"
    )


class EntryEditForm(EntryCreateForm):
    ...


class EntryDetailForm(EntryCreateForm):
    id: PositiveInt = Field(
        default=...,
        title="Entry ID"
    )
