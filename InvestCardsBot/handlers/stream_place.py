# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.inline_keyboards import *

# States
from states.main_states import MainStates


# loader
def load_stream_place_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot

	# main handler
	dispatcher.register_message_handler(
		process_streamPlace_msg,
		filters.Text(equals = "🏛 Invest Place"),
		state = "*"
	)

	dispatcher.register_callback_query_handler(
		process_streamPlace_query,
		lambda x: x.data == "back_to_streamplace",
		state = "*"
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
