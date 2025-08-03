# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.admin.cards_kbs import *
# States
from states.main_states import AdminStates


# loader
def load_admin_cards_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot
	
	### MAIN
	dispatcher.message.register(
		process_cards_main,
		F.Text(equals = "🃏 Карты"),
		StateFilter(AdminStates.main_menu)
	)

	### BACK
	dispatcher.message.register(
		process_cards_main,
		F.Text(equals = "🔙 Назад"),
		StateFilter(
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
		)
	)


async def process_cards_main(message: types.Message, state: FSMContext):

	msg_text = "🃏 Выберите действие:"
	
	await message.answer(
		text = msg_text,
		reply_markup = get_cards_main_kb()
	)

	await AdminStates.cards_main.set()
