# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_influence_categories_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	all_time = InlineKeyboardButton(
		text = "🏆 Рейтинг за все время",
		callback_data = "get_influence_allTime"
	)

	seasonly = InlineKeyboardButton(
		text = "🏆 Рейтинг за сезон",
		callback_data = "get_influence_season"
	)

	back_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(all_time, seasonly, back_btn)

	return inline_markup


def get_back_to_streamplace_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	back_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(back_btn)

	return inline_markup
