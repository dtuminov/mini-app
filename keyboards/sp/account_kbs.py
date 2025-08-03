# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_account_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	back_sp_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(back_sp_btn)

	return inline_markup


def get_back_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	back_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в My Account",
		callback_data = "streamPlace_account"
	)

	inline_markup.add(back_btn)

	return inline_markup