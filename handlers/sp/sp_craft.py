# Aiogram imports
from aiogram import Dispatcher, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.sp.craft_kbs import *

# Database
from database.orm import ORM as orm

# Modules
from modules.cfg_loader import *

# Modules
from modules.duplicates import find_duplicates

# Another
import random
from rich import print
from datetime import datetime


# loader
def load_sp_craft_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot, rarities
	g_bot = bot

	rarities = load_config("./cfg/rarities.json")

	## craft
	dispatcher.callback_query.register(
		process_streamPlace_craft,
		lambda x: x.data == "streamPlace_craft",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		craft_1,
		lambda x: x.data == "craft_1",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		craft_2,
		lambda x: x.data == "craft_2",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		craft_3,
		lambda x: x.data == "craft_3",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		craft_4,
		lambda x: x.data == "craft_4",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		craft_5,
		lambda x: x.data == "craft_5",
		StateFilter('*')
	)


async def process_streamPlace_craft(query: types.CallbackQuery, state: FSMContext):

	classic_cards = await orm.get_cards_ids_by_rarity("classic")
	follower_cards = await orm.get_cards_ids_by_rarity("rare")
	subscriber_cards = await orm.get_cards_ids_by_rarity("superRare")
	legendary_cards = await orm.get_cards_ids_by_rarity("ultraRare")
	stocks_cards = await orm.get_cards_ids_by_rarity("stock")

	inventory = await orm.get_inventory(query.from_user.id)
	my_cards_classic = [x for x in inventory if x in classic_cards]
	my_cards_follower = [x for x in inventory if x in follower_cards]
	my_cards_subscriber = [x for x in inventory if x in subscriber_cards]
	my_cards_legendary = [x for x in inventory if x in legendary_cards]
	my_cards_stocks = [x for x in inventory if x in stocks_cards]

	classic_duplicates = await find_duplicates(my_cards_classic)
	follower_duplicates = await find_duplicates(my_cards_follower)
	subscriber_duplicates = await find_duplicates(my_cards_subscriber)
	legendary_duplicates = await find_duplicates(my_cards_legendary)
	stocks_duplicates = await find_duplicates(my_cards_stocks)

	msg_text = f"""🛠 Здесь вы можете создать попытки или карты выше редкостью из повторных карт

Количество повторных карт:
🟠 Классических: {len(classic_duplicates)}
🟢 Редких: {len(follower_duplicates)}
🔵 Супер-редких: {len(subscriber_duplicates)}
🔴 Ультра-редких: {len(legendary_duplicates)}
📈 Акций: {len(stocks_duplicates)}

10 Классических = 2 попытки
10 Редких = 5 попыток
10 Супер-редких = 9 попыток
10 Ультра-редких = 1 Акция
20 Акций = Настоящая акция"""

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_craft_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def craft_1(query: types.CallbackQuery, state: FSMContext):

	classic_cards = await orm.get_cards_ids_by_rarity("classic")
	my_cards_classic = [x for x in await orm.get_inventory(query.from_user.id) if x in classic_cards]
	classic_duplicates = await find_duplicates(my_cards_classic)

	if len(classic_duplicates) < 10:
		await query.answer(
			text = "❌ Недостаточно дубликатов для крафта!",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return

	user = await orm.get_user(query.from_user.id)

	for duplicate in classic_duplicates[:10]:
		user.inventory.remove(duplicate)

	user.attempts += 2

	await orm.set_users_field(user.user_id, "inventory", list(user.inventory).copy())
	await orm.set_users_field(user.user_id, "attempts", user.attempts)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "craft_1",
		transaction_date = datetime.utcnow(),
		transaction_in = ["attempts", "2"],
		transaction_out = ["cards", ", ".join(map(str, classic_duplicates[:10]))]
	)

	await query.answer(
		text = "✅ Вы скрафтили 2 попытки!",
		show_alert = True
	)

	try:
		await process_streamPlace_craft(query, state)
	except:
		pass

	await g_bot.answer_callback_query(query.id)


async def craft_2(query: types.CallbackQuery, state: FSMContext):

	follower_cards = await orm.get_cards_ids_by_rarity("rare")
	my_cards_follower = [x for x in await orm.get_inventory(query.from_user.id) if x in follower_cards]
	follower_duplicates = await find_duplicates(my_cards_follower)

	if len(follower_duplicates) < 10:
		await query.answer(
			text = "❌ Недостаточно дубликатов для крафта!",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return

	user = await orm.get_user(query.from_user.id)

	for duplicate in follower_duplicates[:10]:
		user.inventory.remove(duplicate)

	user.attempts += 5

	await orm.set_users_field(user.user_id, "inventory", list(user.inventory).copy())
	await orm.set_users_field(user.user_id, "attempts", user.attempts)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "craft_2",
		transaction_date = datetime.utcnow(),
		transaction_in = ["attempts", "5"],
		transaction_out = ["cards", ", ".join(map(str, follower_duplicates[:10]))]
	)

	await query.answer(
		text = "✅ Вы скрафтили 5 попыток!",
		show_alert = True
	)

	try:
		await process_streamPlace_craft(query, state)
	except:
		pass

	await g_bot.answer_callback_query(query.id)


async def craft_3(query: types.CallbackQuery, state: FSMContext):

	subscriber_cards = await orm.get_cards_ids_by_rarity("superRare")
	my_cards_subscriber = [x for x in await orm.get_inventory(query.from_user.id) if x in subscriber_cards]
	subscriber_duplicates = await find_duplicates(my_cards_subscriber)

	if len(subscriber_duplicates) < 10:
		await query.answer(
			text = "❌ Недостаточно дубликатов для крафта!",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return

	user = await orm.get_user(query.from_user.id)

	for duplicate in subscriber_duplicates[:10]:
		user.inventory.remove(duplicate)

	user.attempts += 9

	await orm.set_users_field(user.user_id, "inventory", list(user.inventory).copy())
	await orm.set_users_field(user.user_id, "attempts", user.attempts)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "craft_3",
		transaction_date = datetime.utcnow(),
		transaction_in = ["attempts", "9"],
		transaction_out = ["cards", ", ".join(map(str, subscriber_duplicates[:10]))]
	)

	await query.answer(
		text = "✅ Вы скрафтили 9 попыток!",
		show_alert = True
	)

	try:
		await process_streamPlace_craft(query, state)
	except:
		pass

	await g_bot.answer_callback_query(query.id)


async def craft_4(query: types.CallbackQuery, state: FSMContext):

	legendary_cards = await orm.get_cards_ids_by_rarity("ultraRare")
	my_cards_legendary = [x for x in await orm.get_inventory(query.from_user.id) if x in legendary_cards]
	legendary_duplicates = await find_duplicates(my_cards_legendary)

	if len(legendary_duplicates) < 10:
		await query.answer(
			text = "❌ Недостаточно дубликатов для крафта!",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return

	user = await orm.get_user(query.from_user.id)

	for duplicate in legendary_duplicates[:10]:
		user.inventory.remove(duplicate)

	# get cards
	all_cards_by_rarity = await orm.get_cards_by_rarity_for_drop(rarity = "stock")
	
	# pick random card
	my_new_card = random.choice(all_cards_by_rarity)
	user.points += my_new_card.card_weight
	user.season_points += my_new_card.card_weight

	# add card to inventory
	user.inventory.append(my_new_card.card_id)
	
	# push
	await orm.set_users_field(user.user_id, "inventory", list(user.inventory).copy())
	await orm.set_users_field(user.user_id, "points",  user.points)
	await orm.set_users_field(user.user_id, "season_points", user.season_points)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "craft_4",
		transaction_date = datetime.utcnow(),
		transaction_in = ["card", str(my_new_card.card_id)],
		transaction_out = ["cards", ", ".join(map(str, legendary_duplicates[:10]))]
	)

	await query.answer(
		text = f"✅ Вы скрафтили {my_new_card.card_name} ({rarities.get(my_new_card.card_rarity)})!",
		show_alert = True
	)

	try:
		await process_streamPlace_craft(query, state)
	except:
		pass

	await g_bot.answer_callback_query(query.id)


async def craft_5(query: types.CallbackQuery, state: FSMContext):

	stocks_cards = await orm.get_cards_ids_by_rarity("stock")
	my_cards_subscriber = [x for x in await orm.get_inventory(query.from_user.id) if x in stocks_cards]
	subscriber_duplicates = await find_duplicates(my_cards_subscriber)

	if len(subscriber_duplicates) < 20:
		await query.answer(
			text = "❌ Недостаточно дубликатов для крафта!",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return

	user = await orm.get_user(query.from_user.id)

	for duplicate in subscriber_duplicates[:20]:
		user.inventory.remove(duplicate)

	await orm.set_users_field(user.user_id, "inventory", list(user.inventory).copy())

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "craft_5",
		transaction_date = datetime.utcnow(),
		transaction_in = ["real_stock", "0"],
		transaction_out = ["cards", ", ".join(map(str, subscriber_duplicates[:20]))]
	)

	all_admins = load_config().get("admins")

	for admin in all_admins:
		try:
			await g_bot.send_message(
				chat_id = admin,
				text = f"❗️❗️ Крафт настоящей акции!\n{query.from_user.full_name} (@{query.from_user.username}) (id{query.from_user.id})"
			)
		except:
			pass

	await query.answer(
		text = "✅ Вы скрафтили настоящую акцию! Информация передана администрации.",
		show_alert = True
	)

	try:
		await process_streamPlace_craft(query, state)
	except:
		pass

	await g_bot.answer_callback_query(query.id)