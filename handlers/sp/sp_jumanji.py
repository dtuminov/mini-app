# Aiogram imports
from aiogram import Dispatcher, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.sp.jumanji_kbs import *

# Database
from database.orm import ORM as orm

# Another
import random, asyncio
from rich import print
from datetime import datetime


# loader
def load_sp_jumanji_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot

	## main
	dispatcher.callback_query.register(
		process_streamPlace_jumanji,
		lambda x: x.data == "streamPlace_jumanji" or x.data == "back_to_jumanji",
		StateFilter('*')
	)

	## dice
	dispatcher.callback_query.register(
		process_streamPlace_dice,
		lambda x: x.data == "sp_jumanji_dice",
		StateFilter('*')
	)

	## freecard
	dispatcher.callback_query.register(
		process_streamPlace_freecard,
		lambda x: x.data == "sp_jumanji_freecard",
		StateFilter('*')
	)

	## BOX
	dispatcher.callback_query.register(
		process_streamPlace_box_start,
		lambda x: x.data == "sp_jumanji_box",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_box_play1,
		lambda x: x.data == "box_play",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_box_play2,
		lambda x: x.data.startswith("open_box_"),
		StateFilter('*')
	)

	## CASINO
	dispatcher.callback_query.register(
		process_streamPlace_casino_start,
		lambda x: x.data == "sp_jumanji_casino",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_casino_play1,
		lambda x: x.data == "casino_play",
		StateFilter('*')
	)

	## BOWLING
	dispatcher.callback_query.register(
		process_streamPlace_bowling_start,
		lambda x: x.data == "sp_jumanji_bowling",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_bowling_play1,
		lambda x: x.data == "bowling_play",
		StateFilter('*')
	)

	## BASKET
	dispatcher.callback_query.register(
		process_streamPlace_basket_start,
		lambda x: x.data == "sp_jumanji_basket",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_basket_play1,
		lambda x: x.data == "basket_play",
		StateFilter('*')
	)

	## DARTS
	dispatcher.callback_query.register(
		process_streamPlace_darts_start,
		lambda x: x.data == "sp_jumanji_darts",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_darts_play1,
		lambda x: x.data == "darts_play",
		StateFilter('*')
	)


async def process_streamPlace_jumanji(query: types.CallbackQuery, state: FSMContext):

	msg_text = "✈️ Выберите игру:"
	
	try:
		await query.message.edit_text(
			text = msg_text,
			reply_markup = get_jumanji_ikb()
		)
	except:
		pass

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_dice(query: types.CallbackQuery, state: FSMContext):

	user = await orm.get_user(query.from_user.id)

	if user.freeze != 0:
		await query.answer(f"☃️ Вы заморожены на {user.freeze}ч!", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	# check attempts
	user = await orm.get_user(query.from_user.id)

	if user.jumanji_attempts.get("dice") == 0:
		await query.answer(
			text = "⚠️ У вас закончились броски на этой неделе.",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return
	
	await query.message.edit_reply_markup(None)

	dice = await g_bot.send_dice(query.from_user.id, emoji = "🎲")

	await g_bot.answer_callback_query(query.id)

	await asyncio.sleep(5)

	# db
	user.jumanji_attempts["dice"] -= 1
	await orm.set_users_field(query.from_user.id, "jumanji_attempts", user.jumanji_attempts)
	await orm.set_users_field(query.from_user.id, "attempts", user.attempts + dice.dice.value)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "jumanji_dice",
		transaction_date = datetime.utcnow(),
		transaction_in = ["attempts", str(dice.dice.value)],
		transaction_out = ["dice_attempts", "1"]
	)

	await query.message.answer(
		text = f"✅ На кубике: {dice.dice.value}. Вам было начислено {dice.dice.value} попыток!",
		reply_markup = get_back_ikb()
	)


async def process_streamPlace_freecard(query: types.CallbackQuery, state: FSMContext):

	user = await orm.get_user(query.from_user.id)

	if user.freeze != 0:
		await query.answer(f"☃️ Вы заморожены на {user.freeze}ч!", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	# check attempts
	user = await orm.get_user(query.from_user.id)

	if user.jumanji_attempts.get("freecard") == 0:
		await query.answer(
			text = "⚠️ У вас закончились бесплатные карты на этой неделе.",
			show_alert = True
		)
		await g_bot.answer_callback_query(query.id)
		return
	
	await query.message.edit_reply_markup(None)

	# get cards
	all_cards_by_rarity = await orm.get_cards_by_rarity_for_drop(rarity = "legendary")
	
	# pick random card
	my_new_card = random.choice(all_cards_by_rarity)
	user.points += my_new_card.card_weight
	user.season_points += my_new_card.card_weight

	# add card to inventory
	user.inventory.append(my_new_card.card_id)
	
	# push
	await orm.set_users_field(user.user_id, "inventory", user.inventory)
	await orm.set_users_field(user.user_id, "points",  user.points)
	await orm.set_users_field(user.user_id, "season_points", user.season_points)
	await orm.set_users_field(user.user_id, "stream_points", user.stream_points + my_new_card.card_weight)

	# db
	await orm.set_users_field(query.from_user.id, "freecard_attempts", user.freecard_attempts - 1)

	### CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = query.from_user.id,
		transaction_type = "jumanji_freecard",
		transaction_date = datetime.utcnow(),
		transaction_in = ["card", str(my_new_card.card_id)],
		transaction_out = ["freecard_attempts", "1"]
	)

	# show card
	caption = f"""🪪 {my_new_card.card_name}
👀 Редкость: {my_new_card.card_rarity.title()}
🌐 +{my_new_card.card_weight} Онлайна

Онлайн за все время: {user.points}
Онлайн за текущий стрим: {user.season_points}"""

	with open(my_new_card.card_image, "rb") as image_bin:
		await query.message.answer_photo(
			photo = image_bin,
			caption = caption
		)

	await query.message.answer(
		text = f"✅ Карта была добавлена в вашу коллекцию!",
		reply_markup = get_back_ikb()
	)

	await g_bot.answer_callback_query(query.id)


### BOX
async def process_streamPlace_box_start(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	msg_text = f"""📦 Выберите ячейку и испытайте свою удачу!
	
Попыток: {me.jumanji_attempts.get("box")}"""
	
	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_game_start_ikb(game = "box", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_box_play1(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	# valid
	if me.jumanji_attempts.get("box") == 0:
		await query.answer("⚠️ У вас закончились бесплатные попытки Box на этой неделе.", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	me.jumanji_attempts["box"] -= 1
	await orm.set_users_field(me.user_id, "jumanji_attempts", me.jumanji_attempts)

	msg_text = "📦 Выберите коробку:"

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_box_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_box_play2(query: types.CallbackQuery, state: FSMContext):

	# random prize
	me = await orm.get_user(query.from_user.id)

	attempts = random.randint(1, 3)

	await orm.set_users_field(me.user_id, "attempts", me.attempts + attempts)

	await query.message.edit_text(
		text = f"🔎 {attempts} попыт{'ка' if attempts == 1 else 'ки'}"
	)

	await query.message.answer(
		text = "✅ Выигрыш!",
		reply_markup = get_game_restart_ikb(game = "box", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


### CASINO
async def process_streamPlace_casino_start(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	msg_text = f"""🎰 Вы получите 5 попыток, если автомат выдаст 3 одинаковых символа.

Попыток: {me.jumanji_attempts.get("casino")}"""

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_game_start_ikb(game = "casino", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_casino_play1(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	# valid
	if me.jumanji_attempts.get("casino") == 0:
		await query.answer("⚠️ У вас закончились бесплатные попытки Casino на этой неделе.", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	me.jumanji_attempts["casino"] -= 1
	await orm.set_users_field(me.user_id, "jumanji_attempts", me.jumanji_attempts)

	await query.message.edit_reply_markup()

	slots = await g_bot.send_dice(
		chat_id = query.from_user.id,
		emoji = "🎰"
	)

	await asyncio.sleep(2)

	me = await orm.get_user(query.from_user.id)

	if slots.dice.value in [1, 22, 43, 64]:
		
		await query.message.answer(
			text = "✅ Вы выиграли 5 попыток!",
			reply_markup = get_game_restart_ikb(game = "casino", sum = "Free")
		)
		
		await orm.set_users_field(me.user_id, "attempts", me.attempts + 5)
	else:
		await query.message.answer(
			text = "☹️ Неудача!",
			reply_markup = get_game_restart_ikb(game = "casino", sum = "Free")
		)
		
	await g_bot.answer_callback_query(query.id)


### BOWLING
async def process_streamPlace_bowling_start(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	msg_text = f"""🎳 Вы получите 3 попытки, если собьёте все кегли за 5 игр.

Попыток: {me.jumanji_attempts.get("bowling")}"""

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_game_start_ikb(game = "bowling", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_bowling_play1(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	# valid
	if me.jumanji_attempts.get("bowling") == 0:
		await query.answer("⚠️ У вас закончились бесплатные попытки Bowling на этой неделе.", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	await g_bot.answer_callback_query(query.id)

	me.jumanji_attempts["bowling"] -= 1
	await orm.set_users_field(me.user_id, "jumanji_attempts", me.jumanji_attempts)

	await query.message.edit_reply_markup()

	for _ in range(5):
		bowling = await g_bot.send_dice(
			chat_id = query.from_user.id,
			emoji = "🎳"
		)

		await asyncio.sleep(3.7)

		if bowling.dice.value == 6:
			me = await orm.get_user(query.from_user.id)

			await query.message.answer(
				text = "✅ Вы выиграли 3 попытки!",
				reply_markup = get_game_restart_ikb(game = "bowling", sum = "Free")
			)
			
			await orm.set_users_field(me.user_id, "attempts", me.attempts + 3)
			return
	
	me = await orm.get_user(query.from_user.id)
	await query.message.answer(
		text = "☹️ Неудача!",
		reply_markup = get_game_restart_ikb(game = "bowling", sum = "Free")
	)


### BASKET
async def process_streamPlace_basket_start(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	msg_text = f"""🏀 Вы получите 3 попытки, если забросите 3 мяча из 6.

Попыток: {me.jumanji_attempts.get("basket")}"""
	
	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_game_start_ikb(game = "basket", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_basket_play1(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	# valid
	if me.jumanji_attempts.get("basket") == 0:
		await query.answer("⚠️ У вас закончились бесплатные попытки Basket на этой неделе.", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	await g_bot.answer_callback_query(query.id)

	me.jumanji_attempts["basket"] -= 1
	await orm.set_users_field(me.user_id, "jumanji_attempts", me.jumanji_attempts)

	await query.message.edit_reply_markup()
	
	success = 0
	for i in range(6):
		basket = await g_bot.send_dice(
			chat_id = query.from_user.id,
			emoji = "🏀"
		)

		await asyncio.sleep(5)

		if basket.dice.value in [4, 5]:
			success += 1

		if success == 3:
			me = await orm.get_user(query.from_user.id)

			await query.message.answer(
				text = "✅ Вы выиграли 3 попытки!",
				reply_markup = get_game_restart_ikb(game = "basket", sum = "Free")
			)
			
			await orm.set_users_field(me.user_id, "attempts", me.attempts + 3)
			await g_bot.answer_callback_query(query.id)
			return
	
	me = await orm.get_user(query.from_user.id)
	await query.message.answer(
		text = "☹️ Неудача!",
		reply_markup = get_game_restart_ikb(game = "basket", sum = "Free")
	)


### DARTS
async def process_streamPlace_darts_start(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	msg_text = f"""🎯 Вы получите 3 попытки, если попадете в центр за 5 игр.

Попыток: {me.jumanji_attempts.get("darts")}"""

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_game_start_ikb(game = "darts", sum = "Free")
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_darts_play1(query: types.CallbackQuery, state: FSMContext):

	me = await orm.get_user(query.from_user.id)

	# valid
	if me.jumanji_attempts.get("darts") == 0:
		await query.answer("⚠️ У вас закончились бесплатные попытки Darts на этой неделе.", show_alert = True)
		await g_bot.answer_callback_query(query.id)
		return

	await g_bot.answer_callback_query(query.id)

	me.jumanji_attempts["darts"] -= 1
	await orm.set_users_field(me.user_id, "jumanji_attempts", me.jumanji_attempts)

	await query.message.edit_reply_markup()

	for i in range(5):
		darts = await g_bot.send_dice(
			chat_id = query.from_user.id,
			emoji = "🎯"
		)

		await asyncio.sleep(3)

		if darts.dice.value == 6:
			me = await orm.get_user(query.from_user.id)

			await query.message.answer(
				text = "✅ Вы выиграли 3 попытки!",
				reply_markup = get_game_restart_ikb(game = "darts", sum = "Free")
			)
			
			await orm.set_users_field(me.user_id, "attempts", me.attempts + 3)
			await g_bot.answer_callback_query(query.id)
			return
	
	me = await orm.get_user(query.from_user.id)
	await query.message.answer(
		text = "☹️ Неудача!",
		reply_markup = get_game_restart_ikb(game = "darts", sum = "Free")
	)