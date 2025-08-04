from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_jumanji_ikb() -> InlineKeyboardMarkup:
    """Клавиатура меню игр Jumanji"""
    buttons = [
        [InlineKeyboardButton(text="📦 Box", callback_data="sp_jumanji_box")],
        [InlineKeyboardButton(text="🎰 Казино", callback_data="sp_jumanji_casino")],
        [InlineKeyboardButton(text="🎳 Боулинг", callback_data="sp_jumanji_bowling")],
        [InlineKeyboardButton(text="🏀 3/6 Basket", callback_data="sp_jumanji_basket")],
        [InlineKeyboardButton(text="🎯 Дартс", callback_data="sp_jumanji_darts")],
        [InlineKeyboardButton(text="🔙 Вернуться в Invest Place", callback_data="back_to_streamplace")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_ikb() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой Назад"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✈️ Назад", callback_data="back_to_jumanji")]
        ]
    )

def get_game_start_ikb(game: str, sum: str) -> InlineKeyboardMarkup:
    """Клавиатура для начала игры"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"▶️ Начать - {sum}", callback_data=f"{game}_play")],
            [InlineKeyboardButton(text="✈️ Назад", callback_data="back_to_jumanji")]
        ]
    )

def get_game_restart_ikb(game: str, sum: str) -> InlineKeyboardMarkup:
    """Клавиатура для повторной игры"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"▶️ Еще раз - {sum}", callback_data=f"{game}_play")],
            [InlineKeyboardButton(text="✈️ Назад", callback_data="back_to_jumanji")]
        ]
    )

def get_box_ikb() -> InlineKeyboardMarkup:
    """Клавиатура для игры Box"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📦", callback_data="open_box_1"),
                InlineKeyboardButton(text="📦", callback_data="open_box_2"),
                InlineKeyboardButton(text="📦", callback_data="open_box_3")
            ]
        ]
    )