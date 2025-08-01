# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext
from aiogram.types.message import ContentType

# Keyboards
from keyboards.admin.promocodes_kbs import *
from keyboards.inline_keyboards import get_bookList_ikb

# Database
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_promocodes_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot
	
	### MAIN
	dispatcher.register_message_handler(
		process_promocodes_main,
		filters.Text(equals = "🎟 Промокоды"),
		state = AdminStates.main_menu
	)

	### BACK
	dispatcher.register_message_handler(
		process_promocodes_main,
		filters.Text(equals = "🔙 Назад"),
		state = [
			AdminStates.promo_add_enterName,
			AdminStates.promo_add_enterUsages,
			AdminStates.promo_add_enterValue,
			AdminStates.promo_del_enterID
		]
	)

	### ADD PROMO
	dispatcher.register_message_handler(
		add_promocode_enterName,
		filters.Text(equals = "➕🎟 Добавить промокод"),
		state = AdminStates.promo_main
	)

	dispatcher.register_message_handler(
		add_promocode_enterUsages,
		content_types = ContentType.TEXT,
		state = AdminStates.promo_add_enterName
	)

	dispatcher.register_message_handler(
		add_promocode_enterValue,
		content_types = ContentType.TEXT,
		state = AdminStates.promo_add_enterUsages
	)

	dispatcher.register_message_handler(
		add_promocode_finish,
		content_types = ContentType.TEXT,
		state = AdminStates.promo_add_enterValue
	)

	### DEL PROMO
	dispatcher.register_message_handler(
		del_promocode_enterID,
		filters.Text(equals = "➖🎟 Удалить промокод"),
		state = AdminStates.promo_main
	)

	dispatcher.register_message_handler(
		del_promocode_finish,
		content_types = ContentType.TEXT,
		state = AdminStates.promo_del_enterID
	)

	### OPEN LIST
	dispatcher.register_message_handler(
		process_promo_list_msg,
		filters.Text(equals = "👀 Показать список"),
		state = AdminStates.promo_main
	)

	dispatcher.register_callback_query_handler(
		process_promo_list_next_page,
		lambda x: x.data == "promo_list_next_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_promo_list_prev_page,
		lambda x: x.data == "promo_list_prev_page",
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_promo_list_page_status,
		lambda x: x.data == "promo_list_page_status",
		state = "*"
	)


async def process_promocodes_main(message: types.Message, state: FSMContext):

	msg_text = "🎟 Выберите действие:"
	
	await message.answer(
		text = msg_text,
		reply_markup = get_promo_main_kb()
	)

	await AdminStates.promo_main.set()


async def add_promocode_enterName(message: types.Message, state: FSMContext):

	msg_text = "➕ Введите имя промокода:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.promo_add_enterName.set()


async def add_promocode_enterUsages(message: types.Message, state: FSMContext):

	# valid
	if await orm.is_promo_exists_by_name(message.text):
		await message.answer(
			text = "🔴 Ошибка! Промокод с указанным именем уже существует:",
			reply_markup = get_back_kb()
		)
		return

	async with state.proxy() as storage:
		storage["createPromo_name"] = message.text

	msg_text = "➕ Введите кол-во использований промокода:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.promo_add_enterUsages.set()


async def add_promocode_enterValue(message: types.Message, state: FSMContext):

	# validate
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Ошибка! Только цифры:",
			reply_markup = get_back_kb()
		)
		return

	async with state.proxy() as storage:
		storage["createPromo_usages"] = int(message.text)

	msg_text = "➕ Введите значение промокода:\n\n<b>Например:</b>\ncard_50\nattempts_10"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.promo_add_enterValue.set()


async def add_promocode_finish(message: types.Message, state: FSMContext):

	# validate
	if not message.text.startswith("card_") and not message.text.startswith("attempts_"):
		await message.answer(
			text = "🔴 Ошибка! Некорректное значение:",
			reply_markup = get_back_kb()
		)
		return
	
	# unpack
	async with state.proxy() as storage:
		name = storage.get("createPromo_name")
		usages = storage.get("createPromo_usages")
		value = message.text.split("_")

	# create row in db
	await orm.create_promo(
		promocode_name = name,
		promocode_usages = usages,
		promocode_value = value
	)

	await message.answer(
		text = f"✅ Промокод '{name}' добавлен!"
	)

	await process_promocodes_main(message, state)


async def del_promocode_enterID(message: types.Message, state: FSMContext):

	msg_text = "➖ Введите ID промокода:"

	await message.answer(
		text = msg_text,
		reply_markup = get_back_kb()
	)

	await AdminStates.promo_del_enterID.set()


async def del_promocode_finish(message: types.Message, state: FSMContext):

	# validate
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Ошибка! Только цифры:",
			reply_markup = get_back_kb()
		)
		return
	
	promocode_id = int(message.text)

	if not await orm.is_promo_exists(promocode_id):
		await message.answer(
			text = "🔴 Ошибка! Промокод с указанным ID не существует:",
			reply_markup = get_back_kb()
		)
		return
	
	# delete promocode
	await orm.delete_promo(promocode_id = promocode_id)

	await message.answer(
		text = f"✅ Промокод c ID{promocode_id} удален!"
	)

	await process_promocodes_main(message, state)


### OPEN LIST
async def process_promo_list_msg(message: types.Message, state: FSMContext, current_page: int = 0):

	items = await orm.get_all_promo()
	items.sort(key = lambda x: x.promocode_id, reverse = True)

	max_page = len(items) // 10 + (1 if len(items) % 10 != 0 else 0)

	# init msg
	msg_text = f"🎟 <i>Список промокодов</i>\n\n"

	# fill orders
	if len(items) == 0:
		msg_text += "💭 Список пуст."
	else:
		msg_text += "<i>ID промо | Название | Использования | Значение</i>\n\n"
		for item in items[current_page * 10:(current_page + 1) * 10]:
			msg_text += f"<b>№{item.promocode_id}</b>  |  <code>{item.promocode_name}</code>  |  <code>{item.promocode_usages}</code>  |  <code>{'_'.join(item.promocode_value)}</code>\n"
	
	await message.answer(
		text = msg_text,
		reply_markup = get_bookList_ikb(
			prefix = "promo_list",
			page = current_page,
			max_page = max_page,
			is_back = False,
			elements_col = 10,
			ids = [0] if len(items) != 0 else [],
			btns = False
		),
		disable_web_page_preview = True
	)

	# remind msg id
	async with state.proxy() as storage:
		storage["promo_current_page"] = current_page


async def process_promo_list_query(query: types.CallbackQuery, state: FSMContext, current_page: int = 0):

	items = await orm.get_all_promo()
	items.sort(key = lambda x: x.promocode_id, reverse = True)

	max_page = len(items) // 10 + (1 if len(items) % 10 != 0 else 0)

	# init msg
	msg_text = f"🎟 <i>Список промокодов</i>\n\n"

	# fill orders
	if len(items) == 0:
		msg_text += "💭 Список пуст."
	else:
		msg_text += "<i>ID промо | Название | Использования | Значение</i>\n\n"
		for item in items[current_page * 10:(current_page + 1) * 10]:
			msg_text += f"<b>№{item.promocode_id}</b>  |  <code>{item.promocode_name}</code>  |  <code>{item.promocode_usages}</code>  |  <code>{'_'.join(item.promocode_value)}</code>\n"

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_bookList_ikb(
			prefix = "promo_list",
			page = current_page,
			max_page = max_page,
			is_back = False,
			elements_col = 10,
			ids = [0] if len(items) != 0 else [],
			btns = False
		),
		disable_web_page_preview = True
	)

	# remind msg id
	async with state.proxy() as storage:
		storage["promo_current_page"] = current_page


async def process_promo_list_next_page(query: types.CallbackQuery, state: FSMContext):

	# unpack current
	async with state.proxy() as storage:
		current_page = storage.get("promo_current_page", -1)

	await process_promo_list_query(query, state, current_page + 1)

	await g_bot.answer_callback_query(query.id)


async def process_promo_list_prev_page(query: types.CallbackQuery, state: FSMContext):

	# unpack current
	async with state.proxy() as storage:
		current_page = storage.get("promo_current_page", 1)
	
	await process_promo_list_query(query, state, current_page - 1)

	await g_bot.answer_callback_query(query.id)


async def process_promo_list_page_status(query: types.CallbackQuery, state: FSMContext):

	# unpack current
	async with state.proxy() as storage:
		current_page = storage.get("promo_current_page")

	await query.answer(
		text = f"👀 Вы просматриваете {current_page + 1} страницу. Для перемещения по страницам используйте кнопки: ⬅️, ➡️.",
		show_alert = True
	)

	await g_bot.answer_callback_query(query.id)
