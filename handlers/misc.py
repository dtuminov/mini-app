# Aiogram imports
import asyncio
from datetime import datetime

from aiogram import Dispatcher, filters, types, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

# Another
from tasks.tasks import *


# Database

# loader
def load_misc_handler(dispatcher: Dispatcher, bot: Bot):
    # init
    global g_bot
    g_bot = bot

    dispatcher.message.register(
        enter_promocode,
        filters.Command("promo"),
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        close_message,
        lambda x: x.data == "close_message",
        StateFilter('*')
    )

    dispatcher.message.register(
        load_tasks,
        filters.Command("load_tasks"),
        F.from_user.id == 872114089,
        StateFilter('*')
    )


async def enter_promocode(message: types.Message, state: FSMContext):
    promocode_name = message.get_args()

    # get promo obj and me
    me = await orm.get_user(message.from_user.id)
    promocode = await orm.get_promo_by_name(promocode_name)

    if promocode_name in me.promocodes:
        await message.answer("🤨 Указанный промокод уже активирован")
        return

    if promocode is None:
        await message.answer("🤨 Указанный промокод не найден")
        return

    if promocode.promocode_usages == 0:
        await message.answer("🤨 Указанный промокод не актуален")
        return

    me.promocodes.append(promocode_name)
    await orm.set_users_field(me.user_id, "promocodes", me.promocodes)
    await orm.decrement_promo_usages(promocode_name)

    if promocode.promocode_value[0] == "card":
        # validate
        card_id = int(promocode.promocode_value[1])
        card = await orm.get_card_by_cardID(card_id)

        if card is None:
            await message.answer("Ошибка!")
            return

        # add card to inventory
        me.inventory.append(card_id)

        # push update
        await orm.set_users_field(me.user_id, "inventory", me.inventory)
        await orm.set_users_field(me.user_id, "points", me.points + card.card_weight)
        await orm.set_users_field(me.user_id, "season_points", me.season_points + card.card_weight)

        # transaction
        await orm.create_transaction(
            transaction_user_id=message.from_user.id,
            transaction_type="promo_card",
            transaction_date=datetime.utcnow(),
            transaction_in=["card", str(card_id)],
            transaction_out=["promo", promocode_name]
        )

        # info
        await message.answer(
            text=f"✅ Промокод активирован! Добавлена карта {card.card_name} ({card.card_rarity.title()})."
        )
    elif promocode.promocode_value[0] == "attempts":
        attempts = int(promocode.promocode_value[1])
        await orm.set_users_field(me.user_id, "attempts", me.attempts + attempts)

        # transaction
        await orm.create_transaction(
            transaction_user_id=message.from_user.id,
            transaction_type="promo_attempts",
            transaction_date=datetime.utcnow(),
            transaction_in=["attempts", str(attempts)],
            transaction_out=["promo", promocode_name]
        )

        # info
        await message.answer(
            text=f"✅ Промокод активирован! Добавлены попытки - {attempts}."
        )


async def close_message(query: types.CallbackQuery, state: FSMContext):
    try:
        await query.message.delete()
    except:
        pass

    await g_bot.answer_callback_query(query.id)


async def load_tasks(message: types.Message, state: FSMContext):
    loop = asyncio.get_running_loop()

    loop.create_task(every_hour())
    loop.create_task(change_season())
    loop.create_task(every_week())

    await message.answer(
        text="✅ Cycled updates are enabled!"
    )
