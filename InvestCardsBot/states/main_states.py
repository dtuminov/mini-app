# Aiogram imports
from aiogram.dispatcher.filters.state import State, StatesGroup


class MainStates(StatesGroup):
	main = State()
	enter_trade_link = State()


class AdminStates(StatesGroup):

	login = State()
	main_menu = State()

	mailer_menu = State()

	mailer_text_enter_text = State()
	mailer_text_enter_link = State()
	mailer_text_enter_finish = State()

	mailer_image_enter_image = State()
	mailer_image_enter_caption = State()
	mailer_image_enter_link = State()
	mailer_image_enter_finish = State()

	add_admin_choose = State()
	
	add_admin_ADD = State()
	add_admin_DEL = State()

	cards_main = State()

	add_card_enterName = State()
	add_card_enterImage = State()
	add_card_enterRarity = State()
	add_card_enterWeight = State()
	add_card_enterTarget = State()

	edit_card_enterID = State()
	edit_card_enterName = State()
	edit_card_enterImage = State()
	edit_card_enterRarity = State()
	edit_card_enterWeight = State()
	edit_card_enterTarget = State()

	search_user_enterEntity = State()
	search_user_actions = State()
	search_user_enterAttempts = State()
	search_user_enterFreeze = State()
	search_user_enterCard = State()
	search_user_enterdelCard = State()

	promo_main = State()
	promo_add_enterName = State()
	promo_add_enterUsages = State()
	promo_add_enterValue = State()
	promo_del_enterID = State()
