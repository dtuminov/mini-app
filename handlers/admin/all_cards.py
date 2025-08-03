# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# DB
from database.orm import ORM as orm
# Keyboards
from keyboards.admin.cards_kbs import *
from keyboards.inline_keyboards import get_opened_card_ikb
# Modules
from modules.cfg_loader import *
# States
from states.main_states import AdminStates


# loader
def load_admin_all_cards_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot, g_storage, rarities
	g_bot = bot
	g_storage = dispatcher.storage

	rarities = load_config("./cfg/rarities.json")

	# categories	
	dispatcher.message.register(
		allCards_categories_msg,
		F.text == "🃏 Все карты",
		StateFilter(AdminStates.cards_main)
	)

	# Back to categories callback
	dispatcher.callback_query.register(
		allCards_categories_query,
		F.data == "allCards_list_back",
		StateFilter(AdminStates.cards_main)
	)

	# Open list by category callback
	dispatcher.callback_query.register(
		allCards_list_query,
		F.data.startswith("allCards_category_"),
		StateFilter(AdminStates.cards_main)
	)

	# List navigation callbacks
	dispatcher.callback_query.register(
		process_allCards_next,
		F.data == "allCards_list_next_page",
		StateFilter("*")
	)

	dispatcher.callback_query.register(
		process_allCards_prev,
		F.data == "allCards_list_prev_page",
		StateFilter("*")
	)

	dispatcher.callback_query.register(
		process_allCards_page_status,
		F.data == "allCards_list_page_status",
		StateFilter("*")
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