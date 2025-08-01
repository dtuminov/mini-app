# Aiogram imports
from aiogram import Dispatcher, types, filters
from aiogram.dispatcher import FSMContext

# Keyboards
from keyboards.admin.cards_kbs import *

# States
from states.main_states import AdminStates


# loader
def load_admin_cards_handler(dispatcher: Dispatcher):

	# init
	global g_bot
	g_bot = dispatcher.bot
	
	### MAIN
	dispatcher.register_message_handler(
		process_cards_main,
		filters.Text(equals = "🃏 Карты"),
		state = AdminStates.main_menu
	)

	### BACK
	dispatcher.register_message_handler(
		process_cards_main,
		filters.Text(equals = "🔙 Назад"),
		state = [
			AdminStates.add_card_enterName,
			AdminStates.add_card_enterImage,
			AdminStates.add_card_enterRarity,
			AdminStates.add_card_enterWeight,
			AdminStates.add_card_enterTarget,

			AdminStates.edit_card_enterID,
			AdminStates.edit_card_enterName,
			AdminStates.edit_card_enterImage,
			AdminStates.edit_card_enterRarity,
			AdminStates.edit_card_enterWeight,
			AdminStates.edit_card_enterTarget
		]
	)


async def process_cards_main(message: types.Message, state: FSMContext):

	msg_text = "🃏 Выберите действие:"
	
	await message.answer(
		text = msg_text,
		reply_markup = get_cards_main_kb()
	)

	await AdminStates.cards_main.set()
