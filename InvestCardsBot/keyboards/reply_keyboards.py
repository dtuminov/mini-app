# Aiogram imports
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def get_main_kb():

	reply_markup = ReplyKeyboardMarkup(resize_keyboard = True, is_persistent = True, row_width = 2)

	get_card_btn = KeyboardButton(
		text = "🤵🏻‍♂️ Стать инвестором"
	)

	my_cards_btn = KeyboardButton(
		text = "💼 Мои карты"
	)

	stream_place = KeyboardButton(
		text = "🏛 Invest Place"
	)

	reply_markup.add(get_card_btn, my_cards_btn, stream_place)

	return reply_markup
