# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_trade_ikb(user_id: int, target_user_id: int, card_id: int):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	choose_card = InlineKeyboardButton(
		text = "🔄 Выбрать карту для обмена",
		callback_data = f"accept_trade_{user_id}_{card_id}"
	)

	deny_btn = InlineKeyboardButton(
		text = "🧨 Отменить",
		callback_data = f"sendTrade_deny_{target_user_id}"
	)

	inline_markup.add(choose_card, deny_btn)

	return inline_markup


def get_trade2_ikb(user_id: int, target_user_id: int, target_card_id: int, card_id: int):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	choose_card = InlineKeyboardButton(
		text = "✅ Завершить обмен",
		callback_data = f"accept2_trade_{user_id}_{target_card_id}_{card_id}"
	)

	deny_btn = InlineKeyboardButton(
		text = "🧨 Отменить",
		callback_data = f"sendTrade_deny_{target_user_id}"
	)

	inline_markup.add(choose_card, deny_btn)

	return inline_markup


def get_back_to_streamplace_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	back_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(back_btn)

	return inline_markup
