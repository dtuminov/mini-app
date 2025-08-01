# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin_kbs import ReplyKeyboardRemove, get_main_menu_kb

# Another
from modules.cfg_loader import load_config

# States
from states.main_states import AdminStates

# Funcs
from handlers.start import process_start


# loader
def load_admin_main_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Register handlers
	dispatcher.register_message_handler(
		process_login_as_admin,
		filters.Command("admin"),
		state = "*"
	)

	## EXIT
	dispatcher.register_message_handler(
		process_admin_exit,
		filters.Text(equals = ["🔚 Выйти"]),
		state = [AdminStates.login, AdminStates.main_menu]
	)
	###

	## SHOW MAIN MENU
	dispatcher.register_message_handler(
		show_admin_menu,
		filters.Text(equals = ["🔚 Назад", "🔚 Вернуться в меню"]),
		state = [
			AdminStates.mailer_menu,
			AdminStates.add_admin_choose,

			AdminStates.cards_main,

			AdminStates.search_user_enterEntity,
			AdminStates.search_user_actions,

			AdminStates.promo_main
		]
	)
	###


async def process_login_as_admin(message: types.Message, state: FSMContext):

	await message.delete()

	# load admins
	admins = load_config().get("admins")

	if message.from_user.id in admins:
		await show_admin_menu(message, state)
	else:
		await message.answer(
			text = "🤨"
		)


async def process_admin_exit(message: types.Message, state: FSMContext):

	await message.answer(
		text = "🔴",
		reply_markup = ReplyKeyboardRemove()
	)

	await process_start(message, state)


async def show_admin_menu(message: types.Message, state: FSMContext):

	msg_text = "👮‍♂️ Вы находитесь в админ-панели"

	await message.answer(
		text = msg_text,
		reply_markup = get_main_menu_kb()
	)

	await AdminStates.main_menu.set()
