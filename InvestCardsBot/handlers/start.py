# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.reply_keyboards import get_main_kb

# Database
from database.orm import ORM as orm

# States
from states.main_states import MainStates

# Another
import random
from datetime import datetime


# loader
def load_start_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Register handlers
	dispatcher.register_message_handler(
		process_start,
		filters.CommandStart(),
		state = "*"
	)


async def process_start(message: types.Message, state: FSMContext):

	# close previous state
	await state.reset_state()

	# Get user data
	user_id = message.from_user.id
	user_fullname = message.from_user.full_name.replace("<", "&gt;").replace(">", "&lt;")
	user_username = "@" + message.from_user.username if message.from_user.username is not None else "-"

	# Try to create user row in db
	if not await orm.create_user_if_not_exists(
		user_id = user_id,
		username = user_username,
		fullname = user_fullname,
		register_date = datetime.utcnow()
	):
		await orm.set_users_field(user_id, "username", user_username)
		await orm.set_users_field(user_id, "fullname", user_fullname)

	# hello msg
	hello_text = f"""⚜️ Главное меню"""

	await message.answer(
		text = hello_text,
		reply_markup = get_main_kb()
	)

	# set main state
	await MainStates.main.set()
