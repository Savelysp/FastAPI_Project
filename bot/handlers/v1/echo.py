from datetime import datetime, date, time

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from src.dependencies import DBSession
from src.keyboards.reply import main_panel_kb, get_phone_number_kb
from src.keyboards.inline import (
    create_entry_panel_ikb,
    zero_entry_create_ikb,
    MainEntryCallbackData,
    entry_dates_ikb,
    entry_time_ikb,
    EntryDateCallbackData,
    EntryTimeCallbackData
)
from src.models import User, Entry

__all__ = ['router']

router = Router()


@router.message(CommandStart())
async def start(message: Message, session: DBSession):
    user = User(id=message.from_user.id)
    session.add(instance=user)
    try:
        session.commit()
    except IntegrityError:
        text = "Привет! Давно не виделись!"
    else:
        text = "Привет! Я Бот трапеции!"
    finally:
        await message.answer(
            text=text,
            reply_markup=main_panel_kb
        )


@router.message(F.text == '⁉️ СВЯЗЬ С АДМИНИСТРАТОРОМ')
async def support_message(message: Message):
    await message.delete()
    await message.answer(
        text='<a href="https://t.me/IF_mund">Администратор</a>'
    )


@router.message(F.text == '🗒 МОИ ЗАПИСИ')
async def registrations(message: Message):
    user = User(id=message.from_user.id)
    # if not user.phone_number:
    #     await message.answer(
    #         text='введите номер телефона',
    #         reply_markup=get_phone_number_kb
    #     )
    if user.entries:
        await message.answer(
            text=f'Ваши записи:\n\n{user.entries}',
            reply_markup=create_entry_panel_ikb
        )
    else:
        await message.answer(
            text='У вас нет записей',
            reply_markup=zero_entry_create_ikb
        )


@router.message(F.contact)
async def collect_phone(message: Message, session: DBSession):
    await message.delete()
    session.execute(
        update(User)
        .filter_by(id=message.from_user.id)
        .values(phone_number=message.contact.phone_number)
    )
    session.commit()
    await message.answer(
        text='готово',
        reply_markup=main_panel_kb
    )


@router.callback_query(MainEntryCallbackData.filter(F.action == 'create'))
async def choose_date_registration(callback: CallbackQuery):
    await callback.message.edit_text(
        text='выберите подходящюю дату'
    )
    await callback.message.edit_reply_markup(
        reply_markup=entry_dates_ikb()
    )


@router.callback_query(EntryDateCallbackData.filter(F.date_variant))
async def date_registration(callback_date: CallbackQuery):
    await callback_date.message.edit_text(
        text='выберите нужное время'
    )
    await callback_date.message.edit_reply_markup(
        reply_markup=entry_time_ikb()
    )

    @router.callback_query(EntryTimeCallbackData.filter(F.time_variant))
    async def choose_time_registration(callback_time: CallbackQuery, session: DBSession):
        user_registration = Entry(
            entry_time=datetime.combine(
                date(
                    int(callback_date.data[5:9]),
                    int(callback_date.data[10:12]),
                    int(callback_date.data[13:15])
                ),
                time(
                    hour=int(int(callback_time.data[7:-2])/3600)
                )
            )
        )

        user = User(id=callback_time.from_user.id)
        session.add(instance=user_registration)
        session.execute(
            update(Entry)
            .filter_by(entry_time=user_registration)
            .values(user=user)
        )
        session.commit()
        await callback_time.message.edit_text(
            text='запись создана'
        )
