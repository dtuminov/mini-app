# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_craft_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	craft_1_btn = InlineKeyboardButton(
		text = "🟠 Скрафтить из 10 Классических",
		callback_data = "craft_1"
	)

	craft_2_btn = InlineKeyboardButton(
		text = "🟢 Скрафтить из 10 Редких",
		callback_data = "craft_2"
	)

	craft_3_btn = InlineKeyboardButton(
		text = "🔵 Скрафтить из 10 Супер-редких",
		callback_data = "craft_3"
	)

	craft_4_btn = InlineKeyboardButton(
		text = "🔴 Скрафтить из 10 Ультра-редких",
		callback_data = "craft_4"
	)

	craft_5_btn = InlineKeyboardButton(
		text = "📈 Скрафтить из 20 Акций",
		callback_data = "craft_5"
	)

	back_btn = InlineKeyboardButton(
		text = "🔙 Вернуться в Invest Place",
		callback_data = "back_to_streamplace"
	)

	inline_markup.add(craft_1_btn, craft_2_btn, craft_3_btn, craft_4_btn, craft_5_btn, back_btn)

	return inline_markup
