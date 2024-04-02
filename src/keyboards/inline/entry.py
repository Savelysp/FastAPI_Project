from datetime import date, timedelta
from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

__all__ = [
    "create_entry_panel_ikb",
    "zero_entry_create_ikb",
    "MainEntryCallbackData",
    "EntryTimeCallbackData",
    "entry_dates_ikb",
    "entry_time_ikb",
    "EntryDateCallbackData"
]


class MainEntryCallbackData(CallbackData, prefix='entry'):
    action: Literal['create', 'delete', 'phone']


class EntryDateCallbackData(CallbackData, prefix='date'):
    date_variant: date


class EntryTimeCallbackData(CallbackData, prefix='time'):
    time_variant: timedelta


create_entry_panel_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='СОЗДАТЬ ЗАПИСЬ',
                callback_data=MainEntryCallbackData(action='create').pack()
            ),
            InlineKeyboardButton(
                text='ОТМЕНИТЬ ЗАПИСЬ',
                callback_data=MainEntryCallbackData(action='delete').pack()
            )
        ]
    ]
)

zero_entry_create_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='СОЗДАТЬ ЗАПИСЬ',
                callback_data=MainEntryCallbackData(action='create').pack()
            )
        ]
    ]
)


def entry_dates_ikb():
    builder = InlineKeyboardBuilder()
    for i in range(8):
        builder.row(InlineKeyboardButton(
            text=str(date.today() + timedelta(i)),
            callback_data=EntryDateCallbackData(date_variant=date.today() + timedelta(i)).pack()
            )
        )
    return builder.as_markup()


def entry_time_ikb():
    builder = InlineKeyboardBuilder()
    for i in range(10, 23):
        builder.row(InlineKeyboardButton(
            text=str(timedelta(hours=i)),
            callback_data=EntryTimeCallbackData(time_variant=timedelta(hours=i)).pack()
            )
        )
    return builder.as_markup()
