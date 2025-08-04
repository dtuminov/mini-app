from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_influence_categories_ikb() -> InlineKeyboardMarkup:
    """Клавиатура категорий влияния"""
    markup = InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton(
            text="🏆 Рейтинг за все время",
            callback_data="get_influence_allTime"
        ),
        InlineKeyboardButton(
            text="🏆 Рейтинг за сезон",
            callback_data="get_influence_season"
        ),
        InlineKeyboardButton(
            text="🔙 Вернуться в Invest Place",
            callback_data="back_to_streamplace"
        )
    )

    return markup


def get_back_to_streamplace_ikb() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой возврата в Invest Place"""
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton(
            text="🔙 Вернуться в Invest Place",
            callback_data="back_to_streamplace"
        )
    )

    return markup