# speedup
import uvloop
uvloop.install()

# Aiogram imports
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import BotCommand

# Main handlers
from handlers.start import load_start_handler
from handlers.get_card import load_get_card_handler
from handlers.my_cards import load_my_cards_handler
from handlers.stream_place import load_stream_place_handler

# SP
from handlers.sp.sp_influence import load_sp_influence_handler
from handlers.sp.sp_jumanji import load_sp_jumanji_handler
from handlers.sp.sp_craft import load_sp_craft_handler
from handlers.sp.sp_trade import load_sp_trade_handler
from handlers.sp.sp_account import load_sp_account_handler

# Admin
from handlers.admin.main import load_admin_main_handler
from handlers.admin.statistic import load_admin_statistic_handler
from handlers.admin.add_admins import load_admin_add_admins_handler
from handlers.admin.list_of_users import load_get_users_handler
from handlers.admin.mailer import load_admin_mailer_handler
from handlers.admin.cards import load_admin_cards_handler
from handlers.admin.add_card import load_admin_add_card_handler
from handlers.admin.all_cards import load_admin_all_cards_handler
from handlers.admin.recreate_card import load_admin_recreate_card_handler
from handlers.admin.search_user import load_admin_search_user_handler
from handlers.admin.promocodes import load_admin_promocodes_handler

# Misc
from handlers.misc import load_misc_handler

# tasks
from tasks.tasks import *

# My modules
from modules import cfg_loader

# ORM
from database.orm import ORM as orm

# Another imports
import asyncio, logging


# init logging
logging.basicConfig(
	level = logging.INFO,
	format = u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

# Loading cfg
config = cfg_loader.load_config()

# Initialize bot object
bot = Bot(token = config.get("BOT_API_TOKEN"))
bot.parse_mode = "html"

storage = RedisStorage2("127.0.0.1", 6379, db = 5, pool_size = 10, prefix = "invest_cards_bot")
dp = Dispatcher(bot, storage = storage)
start_command = [BotCommand(command = "/start", description = "🔄 Перезапустить бота")]


async def on_shutdown(dp: Dispatcher):
	logging.warning('Shutting down..')

	# Close DB connection (if used)
	await dp.storage.close()
	await dp.storage.wait_closed()

	logging.warning('Bye!')


if __name__ == "__main__":

	# create loop
	loop = asyncio.new_event_loop()
	# set new loop
	asyncio.set_event_loop(loop = loop)

	# Load main handlers
	load_start_handler(
		dispatcher = dp
	)

	load_misc_handler(
		dispatcher = dp
	)

	load_get_card_handler(
		dispatcher = dp
	)

	load_my_cards_handler(
		dispatcher = dp
	)

	## SP
	load_sp_influence_handler(
		dispatcher = dp
	)

	load_sp_jumanji_handler(
		dispatcher = dp
	)

	load_sp_craft_handler(
		dispatcher = dp
	)

	load_sp_trade_handler(
		dispatcher = dp
	)

	load_sp_account_handler(
		dispatcher = dp
	)

	## Load admin's handlers
	load_admin_main_handler(
		dispatcher = dp
	)

	load_admin_statistic_handler(
		dispatcher = dp
	)

	load_admin_add_admins_handler(
		dispatcher = dp
	)

	load_get_users_handler(
		dispatcher = dp
	)

	load_admin_mailer_handler(
		dispatcher = dp
	)

	load_stream_place_handler(
		dispatcher = dp
	)

	load_admin_cards_handler(
		dispatcher = dp
	)

	load_admin_add_card_handler(
		dispatcher = dp
	)

	load_admin_all_cards_handler(
		dispatcher = dp
	)

	load_admin_recreate_card_handler(
		dispatcher = dp
	)

	load_admin_search_user_handler(
		dispatcher = dp
	)

	load_admin_promocodes_handler(
		dispatcher = dp
	)

	loop.create_task(orm.proceed_schemas())
	loop.create_task(bot.set_my_commands(start_command))
	loop.create_task(every_week())
	loop.create_task(every_hour())
	loop.create_task(change_season())

	# Start long-polling
	executor.start_polling(dp, skip_updates = True, on_shutdown = on_shutdown, loop = loop)
