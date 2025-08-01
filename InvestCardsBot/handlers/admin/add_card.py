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
from handlers.admin.cards import process_cards_main


# loader
def load_admin_add_card_handler(dispatcher: Dispatcher):

	# init
	global g_bot, g_storage, rarities
	g_bot = dispatcher.bot
	g_storage = dispatcher.storage
	
	rarities = load_config("./cfg/rarities.json")

	dispatcher.register_message_handler(
		add_card_enterCardName,
		filters.Text(equals = "➕🃏 Добавить карту"),
		state = AdminStates.cards_main
	)

	dispatcher.register_message_handler(
		add_card_enterCardImage,
		content_types = ContentType.TEXT,
		state = AdminStates.add_card_enterName
	)

	dispatcher.register_message_handler(
		add_card_enterCardRarity,
		content_types = ContentType.PHOTO,
		state = AdminStates.add_card_enterImage
	)

	dispatcher.register_message_handler(
		add_card_enterCardWeight,
		filters.Text(equals = ["Классическая", "Редкая", "Супер-редкая", "Ультра-редкая", "Акция"]),
		state = AdminStates.add_card_enterRarity
	)

	dispatcher.register_message_handler(
		add_card_enterCardTarget,
		content_types = ContentType.TEXT,
		state = AdminStates.add_card_enterWeight
	)

	dispatcher.register_message_handler(
		add_card_finish,
		filters.Text(equals = ["Drop", "Limited"]),
		state = AdminStates.add_card_enterTarget
	)


async def add_card_enterCardName(message: types.Message, state: FSMContext):
	
	msg_text = "Введите название карты:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.add_card_enterName.set()


async def add_card_enterCardImage(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["addCard_name"] = message.text

	msg_text = "Отправьте картинку:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.add_card_enterImage.set()


async def add_card_enterCardRarity(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["addCard_image"] = message.photo[-1].file_id

	msg_text = "Выберите редкость карты:"

	await message.answer(
		text = msg_text,
		reply_markup = get_choose_rarity_kb()
	)

	await AdminStates.add_card_enterRarity.set()


async def add_card_enterCardWeight(message: types.Message, state: FSMContext):

	# save card name
	async with state.proxy() as storage:
		storage["addCard_rarity"] = message.text

	msg_text = "Введите вес карты (кол-во баллов):"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.add_card_enterWeight.set()


async def add_card_enterCardTarget(message: types.Message, state: FSMContext):

	card_weight = message.text

	# validation
	if not card_weight.isdigit():
		await message.answer("Только цифры! Повторите попытку:")
		return

	# save card name
	async with state.proxy() as storage:
		storage["addCard_weight"] = int(card_weight)

	msg_text = "Выберите параметр:"

	await message.answer(
		text = msg_text,
		reply_markup = get_choose_target_kb()
	)

	await AdminStates.add_card_enterTarget.set()


async def add_card_finish(message: types.Message, state: FSMContext):

	card_target = message.text.lower()

	async with state.proxy() as storage:
		card_name = storage.get("addCard_name")
		card_image = storage.get("addCard_image")
		card_rarity = storage.get("addCard_rarity")
		card_weight = storage.get("addCard_weight")

	await orm.create_card(
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
	