# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_promo_main_kb():

	reply_markup = ReplyKeyboardMarkup(resize_keyboard = True, is_persistent = True, row_width = 2)

	show_list_btn = KeyboardButton(
		text = "👀 Показать список"
	)

	add_btn = KeyboardButton(
		text = "➕🎟 Добавить промокод"
	)

	del_btn = KeyboardButton(
		text = "➖🎟 Удалить промокод"
	)

	back_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(show_list_btn)
	reply_markup.add(add_btn, del_btn, back_btn)

	return reply_markup


def get_back_kb():

	reply_markup = ReplyKeyboardMarkup(resize_keyboard = True)

	back_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(back_btn)

	return reply_markup
