# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_main_kb():
    # Создаем кнопки
    get_card_btn = KeyboardButton(text="🤵🏻‍♂️ Стать инвестором")
    my_cards_btn = KeyboardButton(text="💼 Мои карты")
    stream_place = KeyboardButton(text="🏛 Invest Place")

    # Создаем клавиатуру с кнопками
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [get_card_btn, my_cards_btn],  # Первый ряд с двумя кнопками
            [stream_place]  # Второй ряд с одной кнопкой
        ],
        resize_keyboard=True,
        is_persistent=True,
        row_width=2
    )

    return reply_markup