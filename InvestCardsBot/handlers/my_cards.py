# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.inline_keyboards import get_rarity_choose_ikb, get_opened_card_ikb

# Modules
from modules.cfg_loader import *

# Database
from database.orm import ORM as orm


# loader
def load_my_cards_handler(dispatcher: Dispatcher):

	# init
	global g_bot, rarities
	g_bot = dispatcher.bot

	rarities = load_config("./cfg/rarities.json")

	# main handler
	dispatcher.register_message_handler(
		process_myCards_categories_msg,
		filters.Text(equals = "💼 Мои карты"),
		state = "*"
	)

	# pick category
	dispatcher.register_callback_query_handler(
		process_myCards_pickCategory,
		lambda x: x.data.startswith("my_cards_"),
		state = "*"
	)

	# back
	dispatcher.register_callback_query_handler(
		process_myCards_categories_query,
		lambda x: x.data == "opened_cards_back",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_myCards_pickCategory_next,
		lambda x: x.data == "opened_cards_next_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_myCards_pickCategory_prev,
		lambda x: x.data == "opened_cards_prev_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_myCards_pickCategory_page_status,
		lambda x: x.data == "opened_cards_page_status",
		state = "*"
	)


async def process_myCards_categories_msg(message: types.Message, state: FSMContext):

	await state.reset_data()

	msg_text = f"💼 Выберите редкость карт:"

	await message.answer(
		text = msg_text,
		reply_markup = get_rarity_choose_ikb()
	)


async def process_myCards_categories_query(query: types.CallbackQuery, state: FSMContext):

	# reset rarity
	await state.reset_data()

	await query.message.delete()

	msg_text = f"💼 Выберите редкость карт:"

	await query.message.answer(
		text = msg_text,
		reply_markup = get_rarity_choose_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def process_myCards_pickCategory(query: types.CallbackQuery, state: FSMContext):

	if query.data.startswith("my_cards_"):
		rarity = query.data.split("_")[-1]
		offset = 0

		# save data
		async with state.proxy() as storage:
			storage["my_cards_rarity"] = rarity
			storage["my_cards_offset"] = offset
	else:
		async with state.proxy() as storage:
			rarity = storage.get("my_cards_rarity")
			offset = storage.get("my_cards_offset")

	if rarity is None or offset is None:
		await query.answer("Ошибка!")
		await g_bot.answer_callback_query(query.id)
		return

	# get cards for this rarity
	all_cards_by_rarity = [x.card_id for x in await orm.get_cards_by_rarity(rarity)]
	my_cards_by_rarity = [x for x in await orm.get_inventory(query.from_user.id) if x in all_cards_by_rarity]
	
	# get unique values
	my_cards_by_rarity_unique = list(set(my_cards_by_rarity))
	my_cards_by_rarity_unique.sort()

	if len(my_cards_by_rarity) == 0:
		await query.answer("☹️ У вас еще нет карт выбранной редкости")
		await g_bot.answer_callback_query(query.id)
		return
	
	if offset >= len(my_cards_by_rarity_unique):
		offset = 0
		async with state.proxy() as storage:
			storage["my_cards_offset"] = offset
	nl = "\n"
	# get 
	card_to_show = await orm.get_card_by_cardID(my_cards_by_rarity_unique[offset])
	caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}{nl + "<b>💎 Limited</b>" if card_to_show.card_target == "limited" else ""}
💸 +{card_to_show.card_weight}₽

🃏 Количество: {my_cards_by_rarity.count(card_to_show.card_id)}"""

	if query.data.startswith("my_cards_"):
		try:
			await query.message.delete()
		except:
			pass

		await query.message.answer_photo(
			photo = card_to_show.card_image,
			caption = caption,
			reply_markup = get_opened_card_ikb(offset = offset, max_offset = len(my_cards_by_rarity_unique))
		)
	else:
		await query.message.edit_media(
			media = types.InputMediaPhoto(media = card_to_show.card_image, caption = caption),
			reply_markup = get_opened_card_ikb(
				offset = offset,
				max_offset = len(my_cards_by_rarity_unique)
			)
		)

	await g_bot.answer_callback_query(query.id)


async def process_myCards_pickCategory_next(query: types.CallbackQuery, state: FSMContext):

	async with state.proxy() as storage:
		storage["my_cards_offset"] = storage.get("my_cards_offset", -1) + 1

	await process_myCards_pickCategory(query, state)

	await g_bot.answer_callback_query(query.id)


async def process_myCards_pickCategory_prev(query: types.CallbackQuery, state: FSMContext):

	async with state.proxy() as storage:
		storage["my_cards_offset"] = storage.get("my_cards_offset", 1) - 1

	await process_myCards_pickCategory(query, state)

	await g_bot.answer_callback_query(query.id)


async def process_myCards_pickCategory_page_status(query: types.CallbackQuery, state: FSMContext):

	await g_bot.answer_callback_query(query.id)
