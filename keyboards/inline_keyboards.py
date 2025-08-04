# Aiogram imports
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_rarity_choose_ikb():
	buttons = [
		[InlineKeyboardButton(text="Классические", callback_data="my_cards_classic")],
		[InlineKeyboardButton(text="Редкие", callback_data="my_cards_rare")],
		[InlineKeyboardButton(text="Супер редкие", callback_data="my_cards_superRare")],
		[InlineKeyboardButton(text="Ультра редкие", callback_data="my_cards_ultraRare")],
		[InlineKeyboardButton(text="Акции", callback_data="my_cards_stock")]
	]

	return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_opened_card_ikb(offset: int, max_offset: int):
	buttons = []

	# Кнопки навигации
	nav_buttons = []
	if offset > 0:
		nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data="opened_cards_prev_page"))

	nav_buttons.append(InlineKeyboardButton(
		text=f"{offset + 1}/{max_offset}",
		callback_data="opened_cards_page_status"
	))

	if offset < max_offset - 1:
		nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data="opened_cards_next_page"))

	if nav_buttons:
		buttons.append(nav_buttons)

	# Кнопка "Назад"
	buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="opened_cards_back")])

	return InlineKeyboardMarkup(inline_keyboard=buttons)
def get_streamplace_ikb():
    buttons = [
        [
            InlineKeyboardButton(
                text="🏆 Influence",
                callback_data="streamPlace_influence"
            )
        ],
        [
            InlineKeyboardButton(
                text="👨‍💻 My account",
                callback_data="streamPlace_account"
            )
        ],
        [
            InlineKeyboardButton(
                text="✈️ Games",
                callback_data="streamPlace_jumanji"
            )
        ],
        [
            InlineKeyboardButton(
                text="🛠 Craft",
                callback_data="streamPlace_craft"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Trade",
                callback_data="streamPlace_trade"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

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
