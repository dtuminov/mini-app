# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_cards_main_kb():

	reply_markup = ReplyKeyboardMarkup(resize_keyboard = True, is_persistent = True, row_width = 2)

	show_list_btn = KeyboardButton(
		text = "🃏 Все карты"
	)

	add_btn = KeyboardButton(
		text = "➕🃏 Добавить карту"
	)

	edit_btn = KeyboardButton(
		text = "✏️🃏 Пересоздать карту"
	)

	back_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(show_list_btn)
	reply_markup.add(add_btn, edit_btn, back_btn)

	return reply_markup


def get_back_kb():

	reply_markup = ReplyKeyboardMarkup(resize_keyboard = True)

	back_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(back_btn)

	return reply_markup


def get_choose_rarity_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		row_width = 2,
		is_persistent = True
	)

	classic_btn = KeyboardButton(
		text = "Классическая"
	)

	privileged_btn = KeyboardButton(
		text = "Редкая"
	)

	bond_btn = KeyboardButton(
		text = "Супер-редкая"
	)

	part_btn = KeyboardButton(
		text = "Ультра-редкая"
	)

	story_btn = KeyboardButton(
		text = "Акция"
	)

	back_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(classic_btn, privileged_btn, bond_btn, part_btn, story_btn)
	reply_markup.add(back_btn)

	return reply_markup


def get_choose_target_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		row_width = 2,
		is_persistent = True
	)

	drop_btn = KeyboardButton(
		text = "Drop"
	)

	limited_btn = KeyboardButton(
		text = "Limited"
	)

	back_btn = KeyboardButton(
		text = "🔙 Назад"
	)

	reply_markup.add(drop_btn, limited_btn)
	reply_markup.add(back_btn)

	return reply_markup


def get_rarity_choose_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	classic_btn = InlineKeyboardButton(
		text = "🟠 Классическая",
		callback_data = "allCards_category_classic"
	)

	rare_btn = InlineKeyboardButton(
		text = "🟢 Редкая",
		callback_data = "allCards_category_rare"
	)

	superRare_btn = InlineKeyboardButton(
		text = "🔵 Супер-редкая",
		callback_data = "allCards_category_superRare"
	)

	ultraRare_btn = InlineKeyboardButton(
		text = "🔴 Ультра-редкая",
		callback_data = "allCards_category_ultraRare"
	)

	stock_btn = InlineKeyboardButton(
		text = "📈 Акция",
		callback_data = "allCards_category_stock"
	)

	inline_markup.add(classic_btn, rare_btn, superRare_btn, ultraRare_btn, stock_btn)

	return inline_markup
