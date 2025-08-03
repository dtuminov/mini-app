# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.admin_kbs import ReplyKeyboardRemove, get_main_menu_kb

# Another
from modules.cfg_loader import load_config

# States
from states.main_states import AdminStates

# Funcs
from handlers.start import process_start


# loader
def load_admin_main_handler(dispatcher: Dispatcher,bot: Bot ):

	# init
	global g_bot
	g_bot = bot

	# Register handlers
	dispatcher.message.register(
		process_login_as_admin,
		filters.Command("admin"),
		StateFilter('*')
	)

	## EXIT
	dispatcher.message.register(
		process_admin_exit,
		F.Text(equals = ["🔚 Выйти"]),
		StateFilter(AdminStates.login, AdminStates.main_menu)
	)
	###

	## SHOW MAIN MENU
	dispatcher.message.register(
		show_admin_menu,
		F.Text(equals = ["🔚 Назад", "🔚 Вернуться в меню"]),
		StateFilter(
			AdminStates.mailer_menu,
			AdminStates.add_admin_choose,
			AdminStates.cards_main,
			AdminStates.search_user_enterEntity,
			AdminStates.search_user_actions,
			AdminStates.promo_main
		)
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
