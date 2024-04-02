from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = [
    'main_panel_kb',
    'get_phone_number_kb'
]

main_panel_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False,
    keyboard=[
        [
            KeyboardButton(
                text='🗒 МОИ ЗАПИСИ'
            ),
            KeyboardButton(
                text='⁉️ СВЯЗЬ С АДМИНИСТРАТОРОМ'
            )
        ]
    ]
)

get_phone_number_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [
            KeyboardButton(
                text='🖋 РЕГИСТРАЦИЯ',
                request_contact=True
            )
        ]
    ]
)
