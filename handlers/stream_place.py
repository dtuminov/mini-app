# Aiogram imports
from aiogram import Dispatcher, filters, types, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.inline_keyboards import *

# States
from states.main_states import MainStates


# loader
def load_stream_place_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot

	# main handler
	dispatcher.message.register(
		process_streamPlace_msg,
		F.Text(equals = "🏛 Invest Place"),
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_query,
		lambda x: x.data == "back_to_streamplace",
		StateFilter('*')
	)


async def process_streamPlace_msg(message: types.Message, state: FSMContext):

	msg_text = "🏛 Выберите действие:"

	await message.answer(
		text = msg_text,
		reply_markup = get_streamplace_ikb()
	)

	await MainStates.main.set()


async def process_streamPlace_query(query: types.CallbackQuery, state: FSMContext):

	msg_text = "🏛 Выберите действие:"

	try:
		await query.message.edit_text(
			text = msg_text,
			reply_markup = get_streamplace_ikb()
		)
	except:
		await query.message.delete()

		await query.message.answer(
			text = msg_text,
			reply_markup = get_streamplace_ikb()
		)
	
	await MainStates.main.set()

	await g_bot.answer_callback_query(query.id)
