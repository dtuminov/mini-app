# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

# DB
from database.orm import ORM as orm
from handlers.admin.cards import process_cards_main
# Keyboards
from keyboards.admin.cards_kbs import *
# Modules
from modules.cfg_loader import *
# States
from states.main_states import AdminStates


# loader
def load_admin_add_card_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot, g_storage, rarities
	g_bot = bot
	g_storage = dispatcher.storage
	
	rarities = load_config("./cfg/rarities.json")

	dispatcher.message.register(
		add_card_enterCardName,
		F.text == "➕🃏 Добавить карту",
		StateFilter(AdminStates.cards_main)
	)

	dispatcher.message.register(
		add_card_enterCardImage,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.add_card_enterName)
	)

	dispatcher.message.register(
		add_card_enterCardRarity,
		F.content_type == ContentType.PHOTO,
		StateFilter(AdminStates.add_card_enterImage)
	)

	dispatcher.message.register(
		add_card_enterCardWeight,
		F.text.in_(["Классическая", "Редкая", "Супер-редкая", "Ультра-редкая", "Акция"]),
		StateFilter(AdminStates.add_card_enterRarity)
	)

	dispatcher.message.register(
		add_card_enterCardTarget,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.add_card_enterWeight)
	)

	dispatcher.message.register(
		add_card_finish,
		F.text.in_(["Drop", "Limited"]),
		StateFilter(AdminStates.add_card_enterTarget)
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
	