# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.reply_keyboards import get_main_kb
from keyboards.inline_keyboards import get_url_ikb

# Database
from database.orm import ORM as orm

# Modules
from modules.cfg_loader import load_config
from modules.time_str import seconds_to_str

# States
from states.main_states import MainStates

# Another
import random, asyncio
from datetime import datetime, timedelta


# loader
def load_get_card_handler(dispatcher: Dispatcher):

	# init
	global g_bot, channel_id, channel_link, rarities
	g_bot = dispatcher.bot

	rarities = load_config("./cfg/rarities.json")

	channel_id = load_config().get("channel_id")
	channel_link = load_config().get("channel_link")

	# main handler
	dispatcher.register_message_handler(
		process_get_card,
		filters.Text(equals = "🤵🏻‍♂️ Стать инвестором"),
		state = MainStates.main
	)


async def process_get_card(message: types.Message, state: FSMContext):

	### RESET STATE
	await state.reset_state(with_data = True)

	### RANDOM DELAY
	await asyncio.sleep(random.uniform(0.5, 1.0))

	### CHECK FREEZE
	user = await orm.get_user(user_id = message.from_user.id)

	if user.freeze != 0:
		await message.answer(f"☃️ Вы заморожены на {user.freeze}ч!")
		await MainStates.main.set()
		return
	###

	### CHECK CHANNEL SUB
	if len(user.inventory) != 0:
		try:
			chat_member = await g_bot.get_chat_member(channel_id, message.from_user.id)
			chat_member_check = isinstance(chat_member, types.ChatMember) and chat_member.status != "left"

			if not chat_member_check:
				await message.answer(
					text = "🔗 Для доступа ко всем возможностям бота необходимо подписаться на канал по кнопке ниже",
					reply_markup = get_url_ikb(channel_link)
				)
				await MainStates.main.set()
				return
		except:
			pass
	###

	### CHECK FREE_ATTEMPT COOLDOWN
	me = await orm.get_user(message.from_user.id)
	
	if datetime.utcnow() >= (user.upd_date + timedelta(hours = 4)):
		user.attempts += 1
		await orm.set_users_field(user.user_id, "attempts", user.attempts)

	### RANDOM DELAY
	await asyncio.sleep(random.uniform(0.2, 0.4))

	### CHECK ATTEMPTS
	if user.attempts == 0:
		await message.answer(
			text = f"⏰ Следущая попытка будет доступна через {seconds_to_str((user.upd_date + timedelta(hours = 4) - datetime.utcnow()).total_seconds())}."
		)
		await MainStates.main.set()
		return
	###

	### GET CARD
	# choose rarity
	random_number = random.randint(1, 200)

	if random_number == 200:
		rarity = "stock"
	if random_number >= 190:
		rarity = "ultraRare"
	elif random_number >= 170:
		rarity = "superRare"
	elif random_number >= 110:
		rarity = "rare"
	else:
		rarity = "classic"

	# get cards
	all_cards_by_rarity = await orm.get_cards_by_rarity_for_drop(rarity = rarity)
	
	# pick random card
	my_new_card = random.choice(all_cards_by_rarity)
	###
	
	### CHECK ATTEMPTS
	user = await orm.get_user(user_id = message.from_user.id)

	if user.attempts == 0:
		await message.answer(
			text = f"⏰ Следущая попытка будет доступна через {seconds_to_str((user.upd_date + timedelta(hours = 4) - datetime.utcnow()).total_seconds())}."
		)
		await MainStates.main.set()
		return
	else:
		await orm.set_users_field(user.user_id, "attempts", user.attempts - 1)
	###

	### COLLECT DATA
	user = await orm.get_user(user_id = message.from_user.id)

	user.inventory.append(my_new_card.card_id)
	user.points += my_new_card.card_weight
	user.season_points += my_new_card.card_weight
	###

	### PUSH TO DB
	await orm.set_users_field(user.user_id, "inventory", user.inventory)
	await orm.set_users_field(user.user_id, "points",  user.points)
	await orm.set_users_field(user.user_id, "season_points", user.season_points)
	await orm.set_users_field(user.user_id, "upd_date", datetime.utcnow())
	###

	### SHOW CARD IN CHAT
	caption = f"""🗞 {my_new_card.card_name}
👀 Редкость: {rarities.get(my_new_card.card_rarity)}
💸 +{my_new_card.card_weight:,}₽

Рублей за все время: {user.points:,}
Рублей за текущий сезон: {user.season_points:,}"""

	if user.attempts <= 0:
		caption += f"\n\n⏰ Следущая попытка будет доступна через 4 часа."
	else:
		caption += f"\n\n🤵🏻‍♂️ У вас есть еще {user.attempts} попыток."

	await message.answer_photo(
		photo = my_new_card.card_image,
		caption = caption,
		reply_markup = get_main_kb()
	)
	###

	## CREATE TRANSACTION
	await orm.create_transaction(
		transaction_user_id = message.from_user.id,
		transaction_type = "get_card",
		transaction_date = datetime.utcnow(),
		transaction_in = ["card", str(my_new_card.card_id)],
		transaction_out = ["attempts", "1"]
	)

	await MainStates.main.set()
