# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_kb():

	reply_markup = ReplyKeyboardMarkup(
		resize_keyboard = True
	)

	exit_btn = KeyboardButton(
		text = "🔚 Вернуться в меню"
	)

	reply_markup.add(exit_btn)

	return reply_markup


def get_actions_ikb(user_id: int):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	transactions_btn = InlineKeyboardButton(
		text = "📋 Транзакции",
		callback_data = f"su_transactions_{user_id}"
	)

	add_attempts_btn = InlineKeyboardButton(
		text = "✏️🔎 Изменить попытки",
		callback_data = f"su_edit_attempts_{user_id}"
	)

	freeze_btn = InlineKeyboardButton(
		text = "✏️☃️ Изменить заморозку",
		callback_data = f"su_edit_freeze_{user_id}"
	)
	
	add_card_btn = InlineKeyboardButton(
		text = "➕🃏 Добавить карту",
		callback_data = f"su_add_card_{user_id}"
	)

	del_card_btn = InlineKeyboardButton(
		text = "➖ Убрать карту",
		callback_data = f"su_del_card_{user_id}"
	)

	inline_markup.add(transactions_btn, add_attempts_btn, freeze_btn, add_card_btn, del_card_btn)

	return inline_markup


def get_back_ikb(user_id: int):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	exit_btn = InlineKeyboardButton(
		text = "🔚 Назад",
		callback_data = f"back_to_su_{user_id}"
	)

	inline_markup.add(exit_btn)

	return inline_markup
