# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_jumanji_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	dice_btn = InlineKeyboardButton(
		text = "🎲 Кубик",
		callback_data = "sp_jumanji_dice"
	)

	casino_btn = InlineKeyboardButton(
		text = "🎰 Казино",
		callback_data = "sp_jumanji_casino"
	)

	bowling_btn = InlineKeyboardButton(
		text = "🎳 Боулинг",
		callback_data = "sp_jumanji_bowling"
	)

	basket_btn = InlineKeyboardButton(
		text = "🏀 3/6 Basket",
		callback_data = "sp_jumanji_basket"
	)

	darts_btn = InlineKeyboardButton(
		text = "🎯 Дартс",
		callback_data = "sp_jumanji_darts"
	)

	loto_btn = InlineKeyboardButton(
		text = "📦 Box",
		callback_data = "sp_jumanji_box"
	)

	back_sp_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(
		loto_btn,
		#dice_btn,
		casino_btn,
		bowling_btn,
		basket_btn,
		darts_btn,
		back_sp_btn
	)

	return inline_markup


def get_back_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	back_btn = InlineKeyboardButton(
		text = "✈️ Назад",
		callback_data = "back_to_jumanji"
	)

	inline_markup.add(back_btn)

	return inline_markup


def get_game_start_ikb(game: str, sum: str):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	play_btn = InlineKeyboardButton(
		text = f"▶️ Начать - {sum}",
		callback_data = game + "_play"
	)

	back_btn = InlineKeyboardButton(
		text = "✈️ Назад",
		callback_data = "back_to_jumanji"
	)

	inline_markup.add(play_btn, back_btn)

	return inline_markup


def get_game_restart_ikb(game: str, sum: str):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	play_btn = InlineKeyboardButton(
		text = f"▶️ Еще раз - {sum}",
		callback_data = game + "_play"
	)

	back_btn = InlineKeyboardButton(
		text = "✈️ Назад",
		callback_data = "back_to_jumanji"
	)

	inline_markup.add(back_btn)

	return inline_markup


def get_box_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 3)

	btn_1 = InlineKeyboardButton(
		text = "📦",
		callback_data = "open_box_1"
	)

	btn_2 = InlineKeyboardButton(
		text = "📦",
		callback_data = "open_box_2"
	)

	btn_3 = InlineKeyboardButton(
		text = "📦",
		callback_data = "open_box_3"
	)

	inline_markup.add(btn_1, btn_2, btn_3)

	return inline_markup


# {3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7 }