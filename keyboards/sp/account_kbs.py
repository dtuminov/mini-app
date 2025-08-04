from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_account_ikb() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(
            text="📊 Моя статистика", 
            callback_data="account_stats"
        )],
        [InlineKeyboardButton(
            text="🎁 Мои награды",
            callback_data="account_rewards"
        )],
        [InlineKeyboardButton(
            text="🔙 Вернуться в Invest Place",
            callback_data="back_to_streamplace"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🔙 Вернуться в My Account",
                callback_data="streamPlace_account"
            )]
        ]
    )