# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_rarity_choose_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	classic_btn = InlineKeyboardButton(
		text = "🟠 Классическая",
		callback_data = "my_cards_classic"
	)

	rare_btn = InlineKeyboardButton(
		text = "🟢 Редкая",
		callback_data = "my_cards_rare"
	)

	superRare_btn = InlineKeyboardButton(
		text = "🔵 Супер-редкая",
		callback_data = "my_cards_superRare"
	)

	ultraRare_btn = InlineKeyboardButton(
		text = "🔴 Ультра-редкая",
		callback_data = "my_cards_ultraRare"
	)

	stock_btn = InlineKeyboardButton(
		text = "📈 Акция",
		callback_data = "my_cards_stock"
	)

	inline_markup.add(classic_btn, rare_btn, superRare_btn, ultraRare_btn, stock_btn)

	return inline_markup


def get_opened_card_ikb(offset: int, max_offset: int, choose_btn: bool = False, current_card_id: int = -1, prefix: str = "opened_cards", target_id: int = -1, back_to_streamplace: bool = False):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	offset += 1

	prev_page_btn = InlineKeyboardButton(
		text = "⬅️",
		callback_data = f"{prefix}_prev_page"
	)

	status_btn = InlineKeyboardButton(
		text = f"{offset}/{max_offset}",
		callback_data = f"{prefix}_page_status"
	)

	next_page_btn = InlineKeyboardButton(
		text = "➡️",
		callback_data = f"{prefix}_next_page"
	)

	back_btn = InlineKeyboardButton(
		text = "🔙 Назад" if not back_to_streamplace else "🔙 Вернуться в Invest Place",
		callback_data = f"{prefix}_back" if not back_to_streamplace else "back_to_streamplace"
	)

	if choose_btn:
		choose_btn = InlineKeyboardButton(
			text = "✅ Выбрать карту",
			callback_data = f"{prefix}_choose_{current_card_id}"
		)
		inline_markup.add(choose_btn)

	if offset == 1 and max_offset == 1:
		inline_markup.add(status_btn)
	elif offset == max_offset:
		inline_markup.row(prev_page_btn, status_btn)
	elif offset == 1:
		inline_markup.row(status_btn, next_page_btn)
	elif offset != 1:
		inline_markup.row(prev_page_btn, status_btn, next_page_btn)

	if not choose_btn:
		inline_markup.add(back_btn)
	else:
		close_btn = InlineKeyboardButton(
			text = "🧨 Отменить",
			callback_data = f"sendTrade_deny_{target_id}"
		)
		inline_markup.add(close_btn)

	return inline_markup


def get_streamplace_ikb():

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	influence_btn = InlineKeyboardButton(
		text = "🏆 Influence",
		callback_data = "streamPlace_influence"
	)

	my_account_btn = InlineKeyboardButton(
		text = "👨‍💻 My account",
		callback_data = "streamPlace_account"
	)

	jumanji_btn = InlineKeyboardButton(
		text = "✈️ Games",
		callback_data = "streamPlace_jumanji"
	)

	craft_btn = InlineKeyboardButton(
		text = "🛠 Craft",
		callback_data = "streamPlace_craft"
	)

	trade_btn = InlineKeyboardButton(
		text = "🔄 Trade",
		callback_data = "streamPlace_trade"
	)

	inline_markup.add(
		influence_btn,
		my_account_btn,
		jumanji_btn,
		craft_btn,
		trade_btn
	)

	return inline_markup


def get_url_ikb(url: str):

	inline_markup = InlineKeyboardMarkup(row_width=1)

	url_btn = InlineKeyboardButton(
		text = "🔗 Подписаться",
		url = url
	)

	inline_markup.add(url_btn)

	return inline_markup


def get_bookList_ikb(prefix: str, page: int, max_page: int, ids: list[int] = [], query_id: int = None, btns: bool = True, is_close: bool = False, elements_col: int = 10, is_back: bool = True):

	inline_markup = InlineKeyboardMarkup(row_width = 1)

	# init list of btns objects
	ids_btns = []
	
	# fill list
	if btns:
		for id in ids[page * elements_col:(page + 1) * elements_col]:
			btn = InlineKeyboardButton(
				text = f"№{id}",
				callback_data = f"{prefix}_pick_{id}" + (f"_{query_id}" if query_id is not None else "")
			)
			ids_btns.append(btn)

		# add btns to markup
		inline_markup.row(*ids_btns)

	page += 1

	prev_page_btn = InlineKeyboardButton(
		text = "⬅️",
		callback_data = f"{prefix}_prev_page" + (f"_{query_id}" if query_id is not None else "")
	)

	status_btn = InlineKeyboardButton(
		text = f"{page}/{max_page}",
		callback_data = f"{prefix}_page_status" + (f"_{query_id}" if query_id is not None else "")
	)

	next_page_btn = InlineKeyboardButton(
		text = "➡️",
		callback_data = f"{prefix}_next_page" + (f"_{query_id}" if query_id is not None else "")
	)

	back_btn = InlineKeyboardButton(
		text = "🔙 Назад",
		callback_data = f"{prefix}_back" + (f"_{query_id}" if query_id is not None else "")
	)

	close_btn = InlineKeyboardButton(
		text = "❌ Закрыть",
		callback_data = "close_message"
	)

	if len(ids) != 0:
		if page == 1 and max_page == 1:
			inline_markup.add(status_btn)
		elif page == max_page:
			inline_markup.row(prev_page_btn, status_btn)
		elif page == 1:
			inline_markup.row(status_btn, next_page_btn)
		elif page != 1:
			inline_markup.row(prev_page_btn, status_btn, next_page_btn)

	if is_close:
		inline_markup.add(close_btn)
	if is_back:
		inline_markup.add(back_btn)

	return inline_markup
