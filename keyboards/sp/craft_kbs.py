from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_craft_ikb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text="🟠 Скрафтить из 10 Классических",
            callback_data="craft_1"
        )],
        [InlineKeyboardButton(
            text="🟢 Скрафтить из 10 Редких",
            callback_data="craft_2"
        )],
        [InlineKeyboardButton(
            text="🔵 Скрафтить из 10 Супер-редких",
            callback_data="craft_3"
        )],
        [InlineKeyboardButton(
            text="🔴 Скрафтить из 10 Ультра-редких",
            callback_data="craft_4"
        )],
        [InlineKeyboardButton(
            text="📈 Скрафтить из 20 Акций",
            callback_data="craft_5"
        )],
        [InlineKeyboardButton(
            text="🔙 Вернуться в Invest Place",
            callback_data="back_to_streamplace"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)