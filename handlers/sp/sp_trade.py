# Aiogram imports
from aiogram import Dispatcher, types, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.message import ContentType

# Keyboards
from keyboards.reply_keyboards import get_main_kb
from keyboards.inline_keyboards import *
from keyboards.sp.trade_kbs import *

# Database
from database.orm import ORM as orm

# Modules
from modules.cfg_loader import load_config

# States
from states.main_states import MainStates

# Another
from rich import print
import asyncio, random
from datetime import datetime


# loader
def load_sp_trade_handler(dispatcher: Dispatcher, bot: Bot):
    # init
    global g_bot, rarities
    g_bot = bot

    rarities = load_config("./cfg/rarities.json")

    ## main
    ## trade
    dispatcher.callback_query.register(
        process_streamPlace_sendTrade,
        lambda x: x.data == "streamPlace_trade",
        StateFilter('*')
    )

    dispatcher.message.register(
        process_streamPlace_sendTradeChooseCard_msg,
        F.content_type == ContentType.TEXT,
        StateFilter(MainStates.enter_trade_link)
    )

    dispatcher.callback_query.register(
        process_streamPlace_sendTradeChooseCard_next,
        lambda x: x.data == "sendTrade_cards_next_page",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_sendTradeChooseCard_prev,
        lambda x: x.data == "sendTrade_cards_prev_page",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_sendTradeChooseCard_status,
        lambda x: x.data == "sendTrade_cards_page_status",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_sendTradeChooseCard_deny,
        lambda x: x.data.startswith("acceptTrade_cards_deny_") or x.data.startswith(
            "sendTrade_cards_deny_") or x.data.startswith("sendTrade_deny_"),
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_sendTradeChooseCard_confirm,
        lambda x: x.data.startswith("sendTrade_cards_choose_"),
        StateFilter('*')
    )

    ## accept trade - 2 step
    dispatcher.callback_query.register(
        process_streamPlace_acceptTradeChooseCard,
        lambda x: x.data.startswith("accept_trade_"),
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_acceptTradeChooseCard_next,
        lambda x: x.data == "acceptTrade_cards_next_page",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_acceptTradeChooseCard_prev,
        lambda x: x.data == "acceptTrade_cards_prev_page",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_acceptTradeChooseCard_status,
        lambda x: x.data == "acceptTrade_cards_page_status",
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_acceptTradeChooseCard_confirm,
        lambda x: x.data.startswith("acceptTrade_cards_choose_"),
        StateFilter('*')
    )

    dispatcher.callback_query.register(
        process_streamPlace_tradeFinish,
        lambda x: x.data.startswith("accept2_trade_"),
        StateFilter('*')
    )


async def process_streamPlace_sendTrade(query: types.CallbackQuery, state: FSMContext):
    me = await orm.get_user(query.from_user.id)

    if me.freeze != 0:
        await query.answer(f"☃️ Вы заморожены на {me.freeze}ч!", show_alert=True)
        await g_bot.answer_callback_query(query.id)
        return

    msg_text = "💬 Введите @ссылку, кому хотите отправить предложение обмена:"

    await query.message.edit_text(
        text=msg_text,
        reply_markup=get_back_to_streamplace_ikb()
    )

    await state.update_data(sendTrade_msgID=query.message.message_id)
    await state.set_state(MainStates.enter_trade_link)
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_msg(message: types.Message, state: FSMContext):
    # validation usernamious
    target_username = message.text

    # unpack
    data = await state.get_data()
    last_msg_id = data.get("sendTrade_msgID")

    try:
        await g_bot.edit_message_reply_markup(
            chat_id=message.chat.id,
            message_id=last_msg_id,
            reply_markup=None
        )
    except:
        pass

    if target_username == "@" + str(message.from_user.username):
        await message.answer(
            text="🔴 Вы не можете отправить трейд самому себе! Повторите попытку:",
            reply_markup=get_back_to_streamplace_ikb()
        )
        return

    if not await orm.is_user_exists_username(target_username):
        await message.answer(
            text="🔴 Пользователь не найден! Повторите попытку:",
            reply_markup=get_back_to_streamplace_ikb()
        )
        return

    await state.update_data(sendTrade_target_username=target_username)
    await message.answer(text="💬 Выберите карту, которую хотите отдать:")

    # get cards for this rarity
    all_cards_by_rarity = [x.card_id for x in await orm.get_cards_by_rarity("stock")]
    my_cards_by_rarity = [x for x in await orm.get_inventory(message.from_user.id) if x in all_cards_by_rarity]

    # get unique values
    my_cards_by_rarity_unique = list(set(my_cards_by_rarity))
    my_cards_by_rarity_unique.sort()

    if len(my_cards_by_rarity_unique) == 0:
        await message.answer("☹️ У вас еще нет карт редкости Акция", reply_markup=get_back_to_streamplace_ikb())
        return

    offset = 0
    await state.update_data(sendTrade_offset=0)

    # get
    card_to_show = await orm.get_card_by_cardID(my_cards_by_rarity_unique[offset])

    caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 +{card_to_show.card_weight}₽

🃏 Количество: {my_cards_by_rarity.count(card_to_show.card_id)}"""

    await message.answer_photo(
        photo=card_to_show.card_image,
        caption=caption,
        reply_markup=get_opened_card_ikb(offset=offset, max_offset=len(my_cards_by_rarity_unique), choose_btn=True,
                                         current_card_id=card_to_show.card_id, prefix="sendTrade_cards")
    )

    await MainStates.main.set()


async def process_streamPlace_sendTradeChooseCard_query(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    offset = data.get("sendTrade_offset", 0)

    # get cards for this rarity
    all_cards_by_rarity = [x.card_id for x in await orm.get_cards_by_rarity("stock")]
    my_cards_by_rarity = [x for x in await orm.get_inventory(query.from_user.id) if x in all_cards_by_rarity]

    # get unique values
    my_cards_by_rarity_unique = list(set(my_cards_by_rarity))
    my_cards_by_rarity_unique.sort()

    if len(my_cards_by_rarity) == 0:
        await query.answer("☹️ У вас еще нет карт выбранной редкости")
        await g_bot.answer_callback_query(query.id)
        return

    if offset >= len(my_cards_by_rarity_unique):
        offset = 0
        await state.update_data(sendTrade_offset=offset)

    # get
    card_to_show = await orm.get_card_by_cardID(my_cards_by_rarity_unique[offset])

    caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 +{card_to_show.card_weight}₽

🃏 Количество: {my_cards_by_rarity.count(card_to_show.card_id)}"""

    await query.message.edit_media(
        media=types.InputMediaPhoto(media=card_to_show.card_image, caption=caption),
        reply_markup=get_opened_card_ikb(
            offset=offset,
            max_offset=len(my_cards_by_rarity_unique),
            prefix="sendTrade_cards",
            current_card_id=card_to_show.card_id,
            choose_btn=True
        )
    )

    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_next(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("sendTrade_offset", 0)
    await state.update_data(sendTrade_offset=current_offset + 1)
    await process_streamPlace_sendTradeChooseCard_query(query, state)
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_prev(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("sendTrade_offset", 0)
    await state.update_data(sendTrade_offset=current_offset - 1)
    await process_streamPlace_sendTradeChooseCard_query(query, state)
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_status(query: types.CallbackQuery, state: FSMContext):
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_deny(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    target = int(query.data.split("_")[-1])

    try:
        await g_bot.send_message(
            chat_id=target,
            text="🧨 Обмен отменен"
        )
    except:
        pass

    hello_text = f"""⚜️ Главное меню"""
    await query.message.answer(
        text=hello_text,
        reply_markup=get_main_kb()
    )

    await MainStates.main.set()
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_sendTradeChooseCard_confirm(query: types.CallbackQuery, state: FSMContext):
    card_id = int(query.data.split("_")[-1])
    data = await state.get_data()
    target_username = data.get("sendTrade_target_username")

    # get
    card_to_show = await orm.get_card_by_cardID(card_id)

    caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 +{card_to_show.card_weight}₽

🔄 Предложение обмена от <a href='https://t.me/{query.from_user.username}'>{query.from_user.full_name.replace("<", "&lt;").replace(">", "&gt;")}</a> 🔄"""

    try:
        await g_bot.send_photo(
            chat_id=(await orm.get_user_byUsername(target_username)).user_id,
            photo=card_to_show.card_image,
            caption=caption,
            reply_markup=get_trade_ikb(user_id=query.from_user.id, card_id=card_id, target_user_id=query.from_user.id)
        )
    except Exception as e:
        print(e)

    await query.message.delete()
    await query.message.answer(
        text=f"✅ Предложение обмена отправлено {target_username}!",
        disable_web_page_preview=True
    )
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_acceptTradeChooseCard(query: types.CallbackQuery, state: FSMContext):
    if query.data.startswith("accept_trade_"):
        await query.message.delete()
        await state.update_data(
            acceptTrade_offset=0,
            acceptTrade_card_id=int(query.data.split("_")[-1]),
            acceptTrade_user_id=int(query.data.split("_")[-2])
        )
        offset = 0
    else:
        data = await state.get_data()
        offset = data.get("acceptTrade_offset", 0)

    await query.answer(text="💬 Выберите карту для встречного предложения:")

    # get cards for this rarity
    all_cards_by_rarity = [x.card_id for x in await orm.get_cards_by_rarity("stock")]
    my_cards_by_rarity = [x for x in await orm.get_inventory(query.from_user.id) if x in all_cards_by_rarity]

    # get unique values
    my_cards_by_rarity_unique = list(set(my_cards_by_rarity))
    my_cards_by_rarity_unique.sort()

    if len(my_cards_by_rarity) == 0:
        await query.message.answer("☹️ У вас еще нет карт выбранной редкости", reply_markup=get_main_kb())
        await state.reset_state()
        await g_bot.answer_callback_query(query.id)
        return

    if offset >= len(my_cards_by_rarity):
        offset = 0
        await state.update_data(acceptTrade_offset=offset)

    # get
    card_to_show = await orm.get_card_by_cardID(my_cards_by_rarity_unique[offset])

    caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 +{card_to_show.card_weight}₽

🃏 Количество: {my_cards_by_rarity.count(card_to_show.card_id)}"""

    data = await state.get_data()
    target_id = data.get("acceptTrade_user_id")

    if query.data.startswith("accept_trade_"):
        await query.message.answer_photo(
            photo=card_to_show.card_image,
            caption=caption,
            reply_markup=get_opened_card_ikb(
                offset=offset,
                max_offset=len(my_cards_by_rarity_unique),
                prefix="acceptTrade_cards",
                current_card_id=card_to_show.card_id,
                choose_btn=True,
                target_id=target_id
            )
        )
    else:
        await query.message.edit_media(
            media=types.InputMediaPhoto(media=card_to_show.card_image, caption=caption),
            reply_markup=get_opened_card_ikb(
                offset=offset,
                max_offset=len(my_cards_by_rarity_unique),
                prefix="acceptTrade_cards",
                current_card_id=card_to_show.card_id,
                choose_btn=True,
                target_id=target_id
            )
        )

    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_acceptTradeChooseCard_next(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("acceptTrade_offset", 0)
    await state.update_data(acceptTrade_offset=current_offset + 1)
    await process_streamPlace_acceptTradeChooseCard(query, state)
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_acceptTradeChooseCard_prev(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_offset = data.get("acceptTrade_offset", 0)
    await state.update_data(acceptTrade_offset=current_offset - 1)
    await process_streamPlace_acceptTradeChooseCard(query, state)
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_acceptTradeChooseCard_status(query: types.CallbackQuery, state: FSMContext):
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_acceptTradeChooseCard_confirm(query: types.CallbackQuery, state: FSMContext):
    card_id = int(query.data.split("_")[-1])
    data = await state.get_data()
    target_id = data.get("acceptTrade_user_id")
    target_card_id = data.get("acceptTrade_card_id")

    if card_id == target_card_id:
        await query.answer(
            text="Вы не можете обменять одинаковую карту!",
            show_alert=True
        )
        await g_bot.answer_callback_query(query.id)
        return

    target_card = await orm.get_card_by_cardID(target_card_id)
    card_to_show = await orm.get_card_by_cardID(card_id)

    caption = f"""🗞 {card_to_show.card_name}
👀 Редкость: {rarities.get(card_to_show.card_rarity)}
💸 +{card_to_show.card_weight}₽

🔄 Встречное предложение от <a href='https://t.me/{query.from_user.username}'>{query.from_user.full_name.replace("<", "&lt;").replace(">", "&gt;")}</a> на вашу <b>{target_card.card_name} ({target_card.card_rarity})</b> 🔄"""

    try:
        await g_bot.send_photo(
            chat_id=target_id,
            photo=card_to_show.card_image,
            caption=caption,
            reply_markup=get_trade2_ikb(user_id=query.from_user.id, target_card_id=target_card_id, card_id=card_id,
                                        target_user_id=query.from_user.id)
        )
    except Exception as e:
        print(e)

    await query.message.delete()
    await query.message.answer(
        text=f"✅ Встречное предложение отправлено!",
        disable_web_page_preview=True
    )
    await g_bot.answer_callback_query(query.id)


async def process_streamPlace_tradeFinish(query: types.CallbackQuery, state: FSMContext):
    await asyncio.sleep(random.uniform(1.0, 3.0))
    query_data = query.data.split("_")

    first_side_UID = query.from_user.id
    first_side_cardID = int(query_data[-2])
    second_side_UID = int(query_data[-3])
    second_side_cardID = int(query_data[-1])

    # validation
    first_side_user = await orm.get_user(first_side_UID)
    second_side_user = await orm.get_user(second_side_UID)

    if first_side_cardID not in first_side_user.inventory or second_side_cardID not in second_side_user.inventory:
        await query.answer(
            text="🧨 Трейд не действителен!",
            show_alert=True
        )
        await query.message.edit_reply_markup(None)
        await g_bot.answer_callback_query(query.id)
        return

    # swap
    first_inventory = list(first_side_user.inventory)
    second_inventory = list(second_side_user.inventory)

    del first_inventory[first_inventory.index(first_side_cardID)]
    del second_inventory[second_inventory.index(second_side_cardID)]

    first_inventory.append(second_side_cardID)
    second_inventory.append(first_side_cardID)

    await orm.set_users_field(first_side_UID, "inventory", first_inventory)
    await orm.set_users_field(second_side_UID, "inventory", second_inventory)

    await query.answer(text="✅")

    try:
        await query.message.delete()
    except:
        pass

    try:
        card = await orm.get_card_by_cardID(card_id=second_side_cardID)
        await query.message.answer_photo(
            photo=card.card_image,
            caption="✅ Обмен завершен, держите свою карту!"
        )
    except:
        pass

    ### CREATE TRANSACTION
    await orm.create_transaction(
        transaction_user_id=first_side_user.user_id,
        transaction_type="trade",
        transaction_date=datetime.utcnow(),
        transaction_in=["card", str(second_side_cardID)],
        transaction_out=["card", str(first_side_cardID), "receiver", str(second_side_user.user_id)]
    )

    try:
        card = await orm.get_card_by_cardID(card_id=first_side_cardID)
        await g_bot.send_photo(
            chat_id=second_side_user.user_id,
            photo=card.card_image,
            caption="✅ Обмен завершен, держите свою карту!"
        )
    except:
        pass

    ### CREATE TRANSACTION
    await orm.create_transaction(
        transaction_user_id=second_side_user.user_id,
        transaction_type="trade",
        transaction_date=datetime.utcnow(),
        transaction_in=["card", str(first_side_cardID)],
        transaction_out=["card", str(second_side_cardID), "receiver", str(first_side_user.user_id)]
    )

    await g_bot.answer_callback_query(query.id)