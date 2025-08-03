# Aiogram imports
from aiogram import Dispatcher, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.sp.influence_kbs import *

# Database
from database.orm import ORM as orm

# Another
from rich import print


# loader
def load_sp_influence_handler(dispatcher: Dispatcher, bot: Bot):

	# init
	global g_bot
	g_bot = bot

	## main
	dispatcher.callback_query.register(
		process_streamPlace_influence,
		lambda x: x.data == "streamPlace_influence",
		StateFilter('*')
	)

	## by all time
	dispatcher.callback_query.register(
		process_streamPlace_influenceAllTime,
		lambda x: x.data == "get_influence_allTime",
		StateFilter('*')
	)

	# by current season
	dispatcher.callback_query.register(
		process_streamPlace_influenceSeason,
		lambda x: x.data == "get_influence_season",
		StateFilter('*')
	)

	dispatcher.callback_query.register(
		process_streamPlace_influenceSeason,
		lambda x: x.data == "get_influence_season",
		StateFilter('*')
	)


async def process_streamPlace_influence(query: types.CallbackQuery, state: FSMContext):

	msg_text = "🏆 Выберите категорию:"

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_influence_categories_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_influenceAllTime(query: types.CallbackQuery, state: FSMContext):

	all_users = await orm.get_all_users()

	all_users.sort(key = lambda x: x.points, reverse = True)

	msg_text = "🏆 Топ-10 игроков за все время:\n\n"

	for i, user in enumerate(all_users[:10], 1):
		msg_text += f"{i}. {user.fullname} - <b>{user.points:,}₽</b>\n"

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_back_to_streamplace_ikb()
	)

	await g_bot.answer_callback_query(query.id)


async def process_streamPlace_influenceSeason(query: types.CallbackQuery, state: FSMContext):

	all_users = await orm.get_all_users()

	all_users.sort(key = lambda x: x.season_points, reverse = True)

	msg_text = "🏆 Топ-10 игроков за текущий сезон:\n\n"

	for i, user in enumerate(all_users[:10], 1):
		msg_text += f"{i}. {user.fullname} - <b>{user.season_points:,}₽</b>\n"

	await query.message.edit_text(
		text = msg_text,
		reply_markup = get_back_to_streamplace_ikb()
	)

	await g_bot.answer_callback_query(query.id)

