# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True,
		row_width = 2
	)

	statistic_btn = KeyboardButton(
		text = "📊 Статистика"
	)

	mailer_btn = KeyboardButton(
		text = "✉️ Рассылка"
	)

	cards_btn = KeyboardButton(
		text = "🃏 Карты"
	)

	search_user_btn = KeyboardButton(
		text = "🔎 Поиск пользователя"
	)

	promocodes_btn = KeyboardButton(
		text = "🎟 Промокоды"
	)

	users_list = KeyboardButton(
		text = "📑 Список пользователей"
	)

	admin_management_btn = KeyboardButton(
		text = "👮‍♂️ Управление админами"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Выйти"
	)

	reply_markup.add(
		statistic_btn, admin_management_btn,
		mailer_btn, users_list,
		cards_btn, search_user_btn,
		promocodes_btn
	)
	reply_markup.row(exit_btn)

	return reply_markup


def get_mailer_menu_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True
	)

	text_btn = KeyboardButton(
		text = "📝 Текст" 
	)

	image_btn = KeyboardButton(
		text = "🖼 Фото"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Назад"
	)

	reply_markup.row(text_btn, image_btn)
	reply_markup.add(exit_btn)

	return reply_markup


def get_mailer_back_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(exit_btn)

	return reply_markup


def get_mailer_back_with_skip_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True
	)

	skip_btn = KeyboardButton(
		text = "↪️ Пропустить"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(skip_btn, exit_btn)

	return reply_markup

def get_mailer_finish_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True
	)

	start_btn = KeyboardButton(
		text = "🟢 Начать рассылку"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(start_btn, exit_btn)

	return reply_markup


def get_mailer_btn_ikb(link: str):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	btn = InlineKeyboardButton(
		text = "🔗 Перейти",
		url = link
	)

	inline_markup.add(btn)

	return inline_markup


def get_add_admins_kb():

	reply_markup = ReplyKeyboardMarkup(
		row_width = 2,
		resize_keyboard = True,
		is_persistent = True
	)

	_1 = KeyboardButton(
		text = "➕ Добавить"
	)

	_2 = KeyboardButton(
		text = "➖ Убрать"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(_1, _2, exit_btn)

	return reply_markup


def get_add_admins_back_kb():

	reply_markup = ReplyKeyboardMarkup(
		row_width = 1,
		resize_keyboard = True
	)

	back_btn = KeyboardButton(
		text = "🔚 Назад"
	)

	reply_markup.add(back_btn)

	return reply_markup


def get_add_promo_finish_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True,
		is_persistent = True
	)

	confirm_btn = KeyboardButton(
		text = "🟢 Подтвердить"
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(confirm_btn, exit_btn)

	return reply_markup
