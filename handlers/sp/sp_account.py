# Aiogram imports
from aiogram import Dispatcher, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.sp.account_kbs import *

# Database
from database.orm import ORM as orm

# Modules
from modules.cfg_loader import *

# Another
from rich import print


# loader
def load_sp_account_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot

	## main
	dispatcher.callback_query.register(
		process_streamPlace_account,
		lambda x: x.data == "streamPlace_account",
		StateFilter('*')
	)


async def process_streamPlace_account(query: types.CallbackQuery, state: FSMContext):

	# get user
	user = await orm.get_user(query.from_user.id)

	msg_text = f"""😎 {query.from_user.full_name if query.from_user.username is None else '@' + query.from_user.username} (<code>id{user.user_id}</code>)

💸 Рублей за все время: <b>{user.points:,}</b>
🍁 Рублей за текущий сезон: <b>{user.points:,}</b>

🔎 Попытки: <b>{user.attempts}</b>
💼 Карт в портфеле: <b>{len(user.inventory)} шт.</b>"""

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_account_ikb(),
		disable_web_page_preview = True
	)

	await g_bot.answer_callback_query(query.id)
