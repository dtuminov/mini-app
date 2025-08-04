# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.state import any_state
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_statistic_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot

	# Register handlers
	dispatcher.message.register(
		process_statistic,
		F.Text(equals = ["📊 Статистика"]),
		StateFilter(any_state)

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
