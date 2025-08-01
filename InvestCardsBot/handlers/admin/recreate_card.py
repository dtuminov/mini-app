# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ContentType
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin.cards_kbs import *

# DB
from database.orm import ORM as orm

# Modules
from modules.cfg_loader import *

# States
from states.main_states import AdminStates

# Funcs
from handlers.admin.cards import process_cards_main


# loader
def load_admin_recreate_card_handler(dispatcher: Dispatcher):

	# init
	global g_bot, rarities
	g_bot = dispatcher.bot
	
	rarities = load_config("./cfg/rarities.json")

	dispatcher.register_message_handler(
		edit_card_enterCardID,
		filters.Text(equals = "✏️🃏 Пересоздать карту"),
		state = AdminStates.cards_main
	)

	dispatcher.register_message_handler(
		edit_card_enterCardName,
		content_types = ContentType.TEXT,
		state = AdminStates.edit_card_enterID
	)

	dispatcher.register_message_handler(
		edit_card_enterCardImage,
		content_types = ContentType.TEXT,
		state = AdminStates.edit_card_enterName
	)

	dispatcher.register_message_handler(
		edit_card_enterCardRarity,
		content_types = ContentType.PHOTO,
		state = AdminStates.edit_card_enterImage
	)

	dispatcher.register_message_handler(
		edit_card_enterCardWeight,
		filters.Text(equals = ["Classic", "Follower", "Subscriber", "Legendary"]),
		state = AdminStates.edit_card_enterRarity
	)

	dispatcher.register_message_handler(
		edit_card_enterCardTarget,
		content_types = ContentType.TEXT,
		state = AdminStates.edit_card_enterWeight
	)

	dispatcher.register_message_handler(
		edit_card_finish,
		filters.Text(equals = ["Drop", "Limited"]),
		state = AdminStates.edit_card_enterTarget
	)


async def edit_card_enterCardID(message: types.Message, state: FSMContext):
	
	msg_text = "Введите ID карты:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.edit_card_enterID.set()


async def edit_card_enterCardName(message: types.Message, state: FSMContext):

	# validate card_id
	if not message.text.replace("#", "").isdigit():
		await message.answer(
			text = "🔴 Отправьте ID карты по формату: #1337 или 1337. Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	card_id = int(message.text.replace("#", ""))

	if not await orm.is_card_exists(card_id):
		await message.answer(
			text = "🔴 Карта с указанным ID не найдена. Повторите попытку:",
			reply_markup = get_back_kb()
		)
		return

	async with state.proxy() as storage:
		storage["editCard_cardID"] = card_id

	msg_text = "Введите название карты:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.edit_card_enterName.set()


async def edit_card_enterCardImage(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["editCard_name"] = message.text

	msg_text = "Отправьте картинку:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.edit_card_enterImage.set()


async def edit_card_enterCardRarity(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["editCard_image"] = message.photo[-1].file_id

	msg_text = "Выберите редкость карты:"

	await message.answer(
		text = msg_text,
		reply_markup = get_choose_rarity_kb()
	)

	await AdminStates.edit_card_enterRarity.set()


async def edit_card_enterCardWeight(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["editCard_rarity"] = message.text

	msg_text = "Введите вес карты (кол-во баллов):"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.edit_card_enterWeight.set()


async def edit_card_enterCardTarget(message: types.Message, state: FSMContext):

	card_weight = message.text

	# validation
	if not card_weight.isdigit():
		await message.answer("Только цифры! Повторите попытку:")
		return

	# save card name
	async with state.proxy() as storage:
		storage["editCard_weight"] = int(card_weight)

	msg_text = "Выберите параметр:"

	await message.answer(
		text = msg_text,
		reply_markup = get_choose_target_kb()
	)

	await AdminStates.edit_card_enterTarget.set()


async def edit_card_finish(message: types.Message, state: FSMContext):

	card_target = message.text.lower()

	async with state.proxy() as storage:
		card_id = storage.get("editCard_cardID")
		card_name = storage.get("editCard_name")
		card_image = storage.get("editCard_image")
		card_rarity = storage.get("editCard_rarity")
		card_weight = storage.get("editCard_weight")

	await orm.update_card(
		card_id = card_id,
		card_name = card_name,
		card_image = card_image,
		card_weight = card_weight,
		card_rarity = rarities.get(card_rarity),
		card_target = card_target
	)

	await message.answer(
		text = "✅ Карта успешно добавлена!"
	)

	await state.reset_data()

	await process_cards_main(message, state)
