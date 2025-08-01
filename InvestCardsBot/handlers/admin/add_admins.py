# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ParseMode, ContentType
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin_kbs import get_add_admins_kb, get_add_admins_back_kb, ReplyKeyboardRemove

# Another
from modules.cfg_loader import load_config
# DB
from database.orm import ORM as orm
# States
from states.main_states import AdminStates

import simplejson as json

# loader
def load_admin_add_admins_handler(dispatcher: Dispatcher):

	# init
	global g_bot, g_storage
	g_bot = dispatcher.bot
	g_storage = dispatcher.storage
	
	dispatcher.register_message_handler(
		add_admins_choose,
		filters.Text(equals = ["👮‍♂️ Управление админами", "🔚 Назад"]),
		state = [AdminStates.main_menu, AdminStates.add_admin_ADD, AdminStates.add_admin_DEL]
	)

	## ADD ADMIN
	dispatcher.register_message_handler(
		add_admins_ADD_1,
		filters.Text(equals = ["➕ Добавить"]),
		state = AdminStates.add_admin_choose
	)

	dispatcher.register_message_handler(
		add_admins_ADD_2,
		content_types = ContentType.TEXT,
		state = AdminStates.add_admin_ADD
	)

	## DEL ADMIN
	dispatcher.register_message_handler(
		add_admins_DEL_1,
		filters.Text(equals = ["➖ Убрать"]),
		state = AdminStates.add_admin_choose
	)

	dispatcher.register_message_handler(
		add_admins_DEL_2,
		content_types = ContentType.TEXT,
		state = AdminStates.add_admin_DEL
	)


async def add_admins_choose(message: types.Message, state: FSMContext):
	
	admins = load_config().get("admins")

	msg_text = "<i>👮‍♂️ Действующие администраторы</i>\n"

	for admin_id in admins:
		user = await orm.get_user(user_id = admin_id)

		msg_text += f"- {admin_id} | {user.username} | {user.fullname}\n"

	msg_text += f"\n<b>🔽 Выберите действие:</b>"

	await message.answer(
		text = msg_text,
		parse_mode = ParseMode.HTML,
		reply_markup = get_add_admins_kb()
	)

	await AdminStates.add_admin_choose.set()


async def add_admins_ADD_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID нового админа:"""

	await message.answer(
		text = msg_text,
		reply_markup = get_add_admins_back_kb()
	)

	await AdminStates.add_admin_ADD.set()


async def add_admins_ADD_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Только цифры! Повторите попытку:"
		)

		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "🔴 Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	cfg: dict = load_config()
	cfg["admins"].append(admin_id)

	with open("cfg/config.json", "w", encoding="utf-8") as json_file:
		json.dump(cfg, json_file, indent = 4)

	await message.answer("✅ Успешно")

	await add_admins_choose(message, state)


async def add_admins_DEL_1(message: types.Message, state: FSMContext):

	msg_text = f"""Введите ID админа для удаления:"""

	await message.answer(
		text = msg_text,
		parse_mode = ParseMode.HTML,
		reply_markup = get_add_admins_back_kb()
	)

	await AdminStates.add_admin_DEL.set()


async def add_admins_DEL_2(message: types.Message, state: FSMContext):

	# validation
	if not message.text.isdigit():
		await message.answer(
			text = "🔴 Только цифры! Повторите попытку:"
		)

		return

	admin_id = int(message.text)

	if not await orm.is_user_exists(admin_id):
		await message.answer(
			text = "🔴 Пользователь не существует в БД! Повторите попытку:"
		)

		return
	
	# change admin state
	try:
		await g_bot.send_message(
			chat_id = admin_id,
			text = "☹️ Вы больше не являетесь админом!",
			reply_markup = ReplyKeyboardRemove()
		)
	except:
		pass

	try:
		await FSMContext(g_storage, admin_id, admin_id).set_state(None)
	except:
		pass

	cfg: dict = load_config()

	try:
		cfg["admins"].remove(admin_id)

		with open("cfg/config.json", "w", encoding="utf-8") as json_file:
			json.dump(cfg, json_file, indent = 4)

		await message.answer("✅ Успешно")
	except Exception as e:
		await message.answer("🔴 Ошибка!")

	await add_admins_choose(message, state)