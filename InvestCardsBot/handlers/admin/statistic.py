# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.types.message import ParseMode
from aiogram.dispatcher import FSMContext

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_statistic_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# Register handlers
	dispatcher.register_message_handler(
		process_statistic,
		filters.Text(equals = ["📊 Статистика"]),
		state = AdminStates.main_menu
	)


async def process_statistic(message: types.Message, state: FSMContext):
	
	all_users = await orm.get_all_users()

	cards_in_inventories = sum([len(x.inventory) for x in all_users])

	msg_text = f"""<i>📊 Статистика</i>

🔹 Кол-во пользователей в боте: {len(all_users)} чел.
🔹 Кол-во карт в инвентарях: {cards_in_inventories} шт.
🔹 Активных за сегодня: {len(await orm.get_active_users_byToday())} чел.
🔹 Активных за текущую неделю: {len(await orm.get_active_users_byWeek())} чел.
🔹 Активных за текущий месяц: {len(await orm.get_active_users_byMonth())} чел."""

	await message.answer(
		text = msg_text,
		parse_mode = ParseMode.HTML
	)
