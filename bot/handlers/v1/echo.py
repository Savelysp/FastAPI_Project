from datetime import datetime, date, time

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy import update, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.keyboards.reply import main_panel_kb, get_phone_number_kb # noqa
from src.keyboards.inline import (
    create_entry_panel_ikb,
    zero_entry_create_ikb,
    MainEntryCallbackData,
    entry_dates_ikb,
    entry_time_ikb,
    EntryDateCallbackData,
    EntryTimeCallbackData
)
from src.settings import session_maker
from src.models import User, Entry

__all__ = ['router']

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user = User(id=message.from_user.id)
    async with session_maker() as session:  # type: Session
        session.add(instance=user)
        try:
            await session.commit()
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
async def entries(message: Message):
    async with session_maker() as session:  # type: Session
        user = await session.execute(select(User).where(User.id == message.from_user.id))

    # if not user.phone_number:
    #     await message.answer(
    #         text='введите номер телефона',
    #         reply_markup=get_phone_number_kb
    #     )
        try:
            if user.entries:
                await message.answer(
                    text=f'Ваши записи:\n\n{user.entries}',
                    reply_markup=create_entry_panel_ikb
                )
        except Exception:
            await message.answer(
                text='У вас нет записей',
                reply_markup=zero_entry_create_ikb
            )
    # print('hhh')


@router.message(F.contact)
async def collect_phone(message: Message):
    await message.delete()
    async with session_maker() as session:  # type: Session
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
async def choose_date_entry(callback: CallbackQuery):
    await callback.message.edit_text(
        text='выберите подходящюю дату'
    )
    await callback.message.edit_reply_markup(
        reply_markup=entry_dates_ikb()
    )


@router.callback_query(EntryDateCallbackData.filter(F.date_variant))
async def date_entry(callback_date: CallbackQuery):
    await callback_date.message.edit_text(
        text='выберите нужное время'
    )
    await callback_date.message.edit_reply_markup(
        reply_markup=entry_time_ikb()
    )

    @router.callback_query(EntryTimeCallbackData.filter(F.time_variant))
    async def choose_time_entry(callback_time: CallbackQuery):
        user_entry = Entry(
            entry_time=datetime.combine(
                date(
                    int(callback_date.data[5:9]),
                    int(callback_date.data[10:12]),
                    int(callback_date.data[13:15])
                ),
                time(
                    hour=int(int(callback_time.data[7:-2])/3600)
                )
            ),
            user_id=callback_time.from_user.id,
        )

        await callback_time.message.edit_text(
            text='запись создана'
        )
