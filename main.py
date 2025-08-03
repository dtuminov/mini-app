# speedup
import uvloop

uvloop.install()

# Aiogram imports
from aiogram.client.default import DefaultBotProperties

# Aiogram imports
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
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
import asyncio
import logging

# init logging
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)

# Loading cfg
config = cfg_loader.load_config()

# Initialize bot object
bot = Bot(
    token="6679023601:AAEPdQ-FgxBqf0LcZWRs4hw3FGSs0KzoKCw",
    default=DefaultBotProperties(parse_mode="HTML")
)

storage = RedisStorage.from_url("redis://127.0.0.1:6379/5")
dp = Dispatcher(storage=storage)
start_command = [BotCommand(command="/start", description="🔄 Перезапустить бота")]


async def on_startup():
    await bot.set_my_commands(start_command)
    await orm.proceed_schemas()
    asyncio.create_task(every_week())
    asyncio.create_task(every_hour())
    asyncio.create_task(change_season())


async def on_shutdown():
    logging.warning('Shutting down..')
    await dp.storage.close()
    logging.warning('Bye!')


def setup_handlers():
    """Register all handlers with bot instance"""
    # Load main handlers
    load_start_handler(dp)
    load_misc_handler(dp, bot)
    load_get_card_handler(dp, bot)
    load_my_cards_handler(dp, bot)

    # SP handlers
    load_sp_influence_handler(dp, bot)
    load_sp_jumanji_handler(dp, bot)
    load_sp_craft_handler(dp, bot)
    load_sp_trade_handler(dp, bot)
    load_sp_account_handler(dp, bot)

    # Admin handlers
    load_admin_main_handler(dp, bot)
    load_admin_statistic_handler(dp, bot)
    load_admin_add_admins_handler(dp, bot)
    load_get_users_handler(dp, bot)
    load_admin_mailer_handler(dp, bot)
    load_stream_place_handler(dp, bot)
    load_admin_cards_handler(dp, bot)
    load_admin_add_card_handler(dp, bot)
    load_admin_all_cards_handler(dp, bot)
    load_admin_recreate_card_handler(dp, bot)
    load_admin_search_user_handler(dp, bot)
    load_admin_promocodes_handler(dp, bot)


async def main():
    setup_handlers()
    await on_startup()
    await dp.start_polling(bot, on_shutdown=on_shutdown)


if __name__ == "__main__":
    asyncio.run(main())
