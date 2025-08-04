from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_trade_ikb(user_id: int, target_user_id: int, card_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Выбрать карту для обмена",
                    callback_data=f"accept_trade_{user_id}_{card_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧨 Отменить",
                    callback_data=f"sendTrade_deny_{target_user_id}"
                )
            ]
        ]
    )

def get_trade2_ikb(user_id: int, target_user_id: int, target_card_id: int, card_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Завершить обмен",
                    callback_data=f"accept2_trade_{user_id}_{target_card_id}_{card_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧨 Отменить",
                    callback_data=f"sendTrade_deny_{target_user_id}"
                )
            ]
        ]
    )

def get_back_to_streamplace_ikb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Вернуться в Invest Place",
                    callback_data="back_to_streamplace"
                )
            ]
        ]
    )