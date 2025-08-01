# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin.cards_kbs import *
from keyboards.inline_keyboards import get_opened_card_ikb

# Modules
from modules.cfg_loader import *

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_all_cards_handler(dispatcher: Dispatcher):

	# init
	global g_bot, g_storage, rarities
	g_bot = dispatcher.bot
	g_storage = dispatcher.storage

	rarities = load_config("./cfg/rarities.json")

	# categories	
	dispatcher.register_message_handler(
		allCards_categories_msg,
		filters.Text(equals = "🃏 Все карты"),
		state = AdminStates.cards_main
	)

	# back to categories
	dispatcher.register_callback_query_handler(
		allCards_categories_query,
		lambda x: x.data == "allCards_list_back",
		state = AdminStates.cards_main
	)

	# open list by category
	dispatcher.register_callback_query_handler(
		allCards_list_query,
		lambda x: x.data.startswith("allCards_category_"),
		state = AdminStates.cards_main
	)

	# list params
	dispatcher.register_callback_query_handler(
		process_allCards_next,
		lambda x: x.data == "allCards_list_next_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_allCards_prev,
		lambda x: x.data == "allCards_list_prev_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_allCards_page_status,
		lambda x: x.data == "allCards_list_page_status",
		state = "*"
	)


async def allCards_categories_msg(message: types.Message, state: FSMContext):

	# reset rarity
	async with state.proxy() as storage:
		storage["allCards_rarity"] = None

	msg_text = f"🃏 Выберите редкость карт:"

	await message.answer(
		text = msg_text,
		reply_markup = get_rarity_choose_ikb()
	)


async def allCards_categories_query(query: types.CallbackQuery, state: FSMContext):

	# reset rarity
	async with state.proxy() as storage:
		storage["allCards_rarity"] = None

	await query.message.delete()

	msg_text = f"🃏 Выберите редкость карт:"

	await query.message.answer(
		text = msg_text,
		reply_markup = get_rarity_choose_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def allCards_list_query(query: types.CallbackQuery, state: FSMContext):

	if query.data.startswith("allCards_category_"):
		rarity = query.data.split("_")[-1]
		offset = 0

		# save rarity
		async with state.proxy() as storage:
			storage["allCards_rarity"] = rarity
			storage["allCards_offset"] = offset
	else:
		async with state.proxy() as storage:
			rarity = storage.get("allCards_rarity")
			offset = storage.get("allCards_offset", 0)

	if rarity is None:
		await query.answer("Ошибка!", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	# get cards for this rarity
	all_cards_by_rarity = await orm.get_cards_by_rarity(rarity)

	if len(all_cards_by_rarity) == 0:
		await query.answer("Пусто...", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	# valid
	if offset >= len(all_cards_by_rarity):
		async with state.proxy() as storage:
			storage["allCards_offset"] = 0

		offset = 0

	# get 
	card_to_show = all_cards_by_rarity[offset]

	caption = f"""🗞 {card_to_show.card_name} <code>#{card_to_show.card_id}</code>
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 {card_to_show.card_weight}₽
🎯 Цель: {card_to_show.card_target.title()}"""

	if query.data.startswith("allCards_category_"):
		await query.message.delete()
	
		await query.message.answer_photo(
			photo = card_to_show.card_image,
			caption = caption,
			reply_markup = get_opened_card_ikb(
				offset = offset,
				max_offset = len(all_cards_by_rarity),
				prefix = "allCards_list"
			)
		)
	else:
		await query.message.edit_media(
			media = types.InputMediaPhoto(media = card_to_show.card_image, caption = caption),
			reply_markup = get_opened_card_ikb(
				offset = offset,
				max_offset = len(all_cards_by_rarity),
				prefix = "allCards_list"
			)
		)

	await g_bot.answer_callback_query(query.id)


async def process_allCards_next(query: types.CallbackQuery, state: FSMContext):

	async with state.proxy() as storage:
		storage["allCards_offset"] += 1

	await allCards_list_query(query, state)

	await g_bot.answer_callback_query(query.id)


async def process_allCards_prev(query: types.CallbackQuery, state: FSMContext):

	async with state.proxy() as storage:
		storage["allCards_offset"] -= 1

	await allCards_list_query(query, state)

	await g_bot.answer_callback_query(query.id)


async def process_allCards_page_status(query: types.CallbackQuery, state: FSMContext):

	await g_bot.answer_callback_query(query.id)