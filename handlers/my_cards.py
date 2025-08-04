# Aiogram imports
from aiogram import Dispatcher, types, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state

# Keyboards
from keyboards.inline_keyboards import get_rarity_choose_ikb, get_opened_card_ikb

# Modules
from modules.cfg_loader import load_config

# Database
from database.orm import ORM as orm

# Initialize global variables
g_bot = None
rarities = None


def load_my_cards_handler(dispatcher: Dispatcher, bot: Bot):
    global g_bot, rarities
    g_bot = bot
    rarities = load_config("./cfg/rarities.json")

    # Main message handler
    dispatcher.message.register(
        process_my_cards_categories_msg,
        lambda message: message.text == "💼 Мои карты",
        StateFilter(any_state)
    )

    # Callback handlers
    dispatcher.callback_query.register(
        process_my_cards_pick_category,
        lambda x: x.data.startswith("my_cards_"),
        StateFilter(any_state)
    )

    dispatcher.callback_query.register(
        process_my_cards_categories_query,
        lambda x: x.data == "opened_cards_back",
        StateFilter(any_state)
    )

    dispatcher.callback_query.register(
        process_my_cards_pick_category_next,
        lambda x: x.data == "opened_cards_next_page",
        StateFilter(any_state)
    )

    dispatcher.callback_query.register(
        process_my_cards_pick_category_prev,
        lambda x: x.data == "opened_cards_prev_page",
        StateFilter(any_state)
    )

    dispatcher.callback_query.register(
        process_my_cards_page_status,
        lambda x: x.data == "opened_cards_page_status",
        StateFilter(any_state)
    )


async def process_my_cards_categories_msg(message: types.Message, state: FSMContext):
    """Обработчик сообщения с кнопкой 'Мои карты'"""
    await state.clear()  # Очищаем состояние вместо reset_data()

    await message.answer(
        text="💼 Выберите редкость карт:",
        reply_markup=get_rarity_choose_ikb()
    )


async def process_my_cards_categories_query(query: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Назад'"""
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text="💼 Выберите редкость карт:",
        reply_markup=get_rarity_choose_ikb()
    )
    await query.answer()


async def process_my_cards_pick_category(query: types.CallbackQuery, state: FSMContext):
    """Обработчик выбора категории карт"""
    if query.data.startswith("my_cards_"):
        rarity = query.data.split("_")[-1]
        offset = 0
        await state.update_data(
            my_cards_rarity=rarity,
            my_cards_offset=offset
        )
    else:
        data = await state.get_data()
        rarity = data.get("my_cards_rarity")
        offset = data.get("my_cards_offset", 0)

    if not rarity:
        await query.answer("Ошибка выбора категории!")
        return

    # Получаем карты выбранной редкости
    all_cards_by_rarity = [x.card_id for x in await orm.get_cards_by_rarity(rarity)]
    inventory = await orm.get_inventory(query.from_user.id)
    my_cards_by_rarity = [x for x in inventory if x in all_cards_by_rarity]

    if not my_cards_by_rarity:
        await query.answer("☹️ У вас еще нет карт выбранной редкости")
        return

    # Получаем уникальные карты
    unique_cards = sorted(list(set(my_cards_by_rarity)))
    if offset >= len(unique_cards):
        offset = 0
        await state.update_data(my_cards_offset=offset)

    card_to_show = await orm.get_card_by_cardID(unique_cards[offset])
    if not card_to_show:
        await query.answer("Ошибка загрузки карты")
        return

    # Формируем описание карты
    card_count = my_cards_by_rarity.count(card_to_show.card_id)
    caption = (
        f"🗞 {card_to_show.card_name}\n"
        f"👀 Редкость: {rarities.get(card_to_show.card_rarity, 'Неизвестно')}\n"
        f"{'<b>💎 Limited</b>\n' if card_to_show.card_target == 'limited' else ''}"
        f"💸 +{card_to_show.card_weight}₽\n\n"
        f"🃏 Количество: {card_count}"
    )

    try:
        if query.data.startswith("my_cards_"):
            await query.message.delete()
            await query.message.answer_photo(
                photo=card_to_show.card_image,
                caption=caption,
                reply_markup=get_opened_card_ikb(
                    offset=offset,
                    max_offset=len(unique_cards)
                )
            )
        else:
            await query.message.edit_media(
                media=types.InputMediaPhoto(
                    media=card_to_show.card_image,
                    caption=caption
                ),
                reply_markup=get_opened_card_ikb(
                    offset=offset,
                    max_offset=len(unique_cards)
                )
            )
    except Exception as e:
        print(f"Error processing card: {e}")
        await query.answer("Произошла ошибка")

    await query.answer()


async def process_my_cards_pick_category_next(query: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Следующая'"""
    data = await state.get_data()
    offset = data.get("my_cards_offset", 0)
    await state.update_data(my_cards_offset=offset + 1)
    await process_my_cards_pick_category(query, state)
    await query.answer()


async def process_my_cards_pick_category_prev(query: types.CallbackQuery, state: FSMContext):
    """Обработчик кнопки 'Предыдущая'"""
    data = await state.get_data()
    offset = data.get("my_cards_offset", 1)
    await state.update_data(my_cards_offset=offset - 1)
    await process_my_cards_pick_category(query, state)
    await query.answer()


async def process_my_cards_page_status(query: types.CallbackQuery, state: FSMContext):
    """Обработчик статуса страницы"""
    await query.answer()