# Aiogram imports
from aiogram import Dispatcher, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart

# Keyboards
from keyboards.reply_keyboards import get_main_kb

# Database
from database.orm import ORM as orm

# States
from states.main_states import MainStates

# Another
from datetime import datetime


# loader
def load_start_handler(dp: Dispatcher):
    dp.message.register(process_start, CommandStart())



async def process_start(message: Message, state: FSMContext):
    # Очищаем состояние
    await state.clear()

    # Получаем данные пользователя
    user = message.from_user
    user_fullname = user.full_name.replace("<", "&gt;").replace(">", "&lt;")
    user_username = f"@{user.username}" if user.username else "-"

    # Работа с базой данных
    if not await orm.create_user_if_not_exists(
            user_id=user.id,
            username=user_username,
            fullname=user_fullname,
            register_date=message.date
    ):
        await orm.set_users_field(user.id, "username", user_username)
        await orm.set_users_field(user.id, "fullname", user_fullname)

    # Отправляем приветственное сообщение
    await message.answer(
        text="⚜️ Главное меню",
        reply_markup=get_main_kb()
    )
