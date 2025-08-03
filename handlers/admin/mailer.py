# Aiogram imports
from aiogram import Dispatcher, types, filters, Bot, F
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.types import ContentType
from aiogram.fsm.context import FSMContext

# Keyboards
from keyboards.admin_kbs import get_mailer_menu_kb, get_mailer_back_kb, get_mailer_back_with_skip_kb, get_mailer_finish_kb, get_mailer_btn_ikb, get_main_menu_kb

# DB
from database.orm import ORM as orm

# States
from states.main_states import AdminStates


# loader
def load_admin_mailer_handler(dispatcher: Dispatcher,bot: Bot):

	# init
	global g_bot
	g_bot = bot

	# Register handlers
	dispatcher.message.register(
		process_mailer_menu,
		F.text.in_(["✉️ Рассылка", "🔚 Вернуться в меню"]),
		StateFilter(
			AdminStates.main_menu,
			AdminStates.mailer_text_enter_text,
			AdminStates.mailer_text_enter_link,
			AdminStates.mailer_text_enter_finish,
			AdminStates.mailer_image_enter_image,
			AdminStates.mailer_image_enter_caption,
			AdminStates.mailer_image_enter_link,
			AdminStates.mailer_image_enter_finish
		)
	)

	## Текстовая рассылка
	dispatcher.message.register(
		process_mailer_text_1,
		F.text == "📝 Текст",
		StateFilter(AdminStates.mailer_menu)
	)

	dispatcher.message.register(
		process_mailer_text_2,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.mailer_text_enter_text)
	)

	dispatcher.message.register(
		process_mailer_text_3,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.mailer_text_enter_link)
	)

	dispatcher.message.register(
		process_mailer_text_finish,
		F.text == "🟢 Начать рассылку",
		StateFilter(AdminStates.mailer_text_enter_finish)
	)

	## Рассылка с изображением
	dispatcher.message.register(
		process_mailer_image_1,
		F.text == "🖼 Фото",
		StateFilter(AdminStates.mailer_menu)
	)

	dispatcher.message.register(
		process_mailer_image_2,
		F.content_type == ContentType.PHOTO,
		StateFilter(AdminStates.mailer_image_enter_image)
	)

	dispatcher.message.register(
		process_mailer_image_3,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.mailer_image_enter_caption)
	)

	dispatcher.message.register(
		process_mailer_image_4,
		F.content_type == ContentType.TEXT,
		StateFilter(AdminStates.mailer_image_enter_link)
	)

	dispatcher.message.register(
		process_mailer_image_finish,
		F.text == "🟢 Начать рассылку",
		StateFilter(AdminStates.mailer_image_enter_finish)
	)


async def process_mailer_menu(message: types.Message, state: FSMContext):
	
	msg_text = "Выберите тип рассылки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_menu_kb()
	)

	await AdminStates.mailer_menu.set()


async def process_mailer_text_1(message: types.Message, state: FSMContext):

	msg_text = "Введите текст рассылки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_back_kb()
	)

	await AdminStates.mailer_text_enter_text.set()


async def process_mailer_text_2(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_text"] = message.html_text
		print(message.html_text)

	msg_text = "Введите ссылку для кнопки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_back_with_skip_kb()
	)

	await AdminStates.mailer_text_enter_link.set()


async def process_mailer_text_3(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_link"] = message.text if message.text != "↪️ Пропустить" else None
		text = storage.get("admin_mailer_text")

	await message.answer(
		text = "👀 Предпросмотр:",
		reply_markup = get_mailer_finish_kb()
	)

	try:
		await message.answer(
			text = text,
			reply_markup = get_mailer_btn_ikb(link = message.text) if message.text != "↪️ Пропустить" else None,
			parse_mode = ParseMode.HTML
		)
	except:
		await message.answer(
			text = "🔴 Ошибка!",
			reply_markup = get_mailer_menu_kb()
		)

		await AdminStates.mailer_menu.set()
		return


	await AdminStates.mailer_text_enter_finish.set()


async def process_mailer_text_finish(message: types.Message, state: FSMContext):

	# unpack
	async with state.proxy() as storage:
		text = storage.get("admin_mailer_text")
		link = storage.get("admin_mailer_link")

	all_users = await orm.get_all_users()

	counter = 0

	await message.answer(
		text = "▶️ Рассылка запущена...",
		reply_markup = get_main_menu_kb()
	)

	await AdminStates.main_menu.set()

	for user in all_users:
		try:
			await g_bot.send_message(
				chat_id = user.user_id,
				text = text,
				parse_mode = ParseMode.HTML,
				reply_markup = get_mailer_btn_ikb(link) if link is not None else None
			)

			counter += 1
		except Exception as e:
			print(e)

	await message.answer(
		text = f"✅ Рассылка завершена! Сообщение отправлено {counter}/{len(all_users)}."
	)





















async def process_mailer_image_1(message: types.Message, state: FSMContext):

	msg_text = "Отправьте картинку:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_back_kb()
	)

	await AdminStates.mailer_image_enter_image.set()


async def process_mailer_image_2(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_image"] = message.photo[-1].file_id

	msg_text = "Введите описание к фото:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_back_with_skip_kb()
	)

	await AdminStates.mailer_image_enter_caption.set()


async def process_mailer_image_3(message: types.Message, state: FSMContext):

	# validation
	if len(message.text) > 1024:
		await message.answer("🔴 Допустимый лимит символов - 1024. Повторите попытку:")
		return

	async with state.proxy() as storage:
		storage["admin_mailer_caption"] = message.html_text if message.text != "↪️ Пропустить" else None


	msg_text = "Введите ссылку для кнопки:"

	await message.answer(
		text = msg_text,
		reply_markup = get_mailer_back_with_skip_kb()
	)

	await AdminStates.mailer_image_enter_link.set()


async def process_mailer_image_4(message: types.Message, state: FSMContext):

	async with state.proxy() as storage:
		storage["admin_mailer_link"] = message.text if message.text != "↪️ Пропустить" else None
		caption = storage.get("admin_mailer_caption")
		photo = storage.get("admin_mailer_image")

	await message.answer(
		text = "👀 Предпросмотр:",
		reply_markup = get_mailer_finish_kb()
	)

	try:
		await message.answer_photo(
			photo = photo,
			caption = caption,
			reply_markup = get_mailer_btn_ikb(link = message.text) if message.text != "↪️ Пропустить" else None,
			parse_mode = ParseMode.HTML
		)
	except Exception as e:
		print(e)
		await message.answer(
			text = "🔴 Ошибка!",
			reply_markup = get_mailer_menu_kb()
		)

		await AdminStates.mailer_menu.set()
		return


	await AdminStates.mailer_image_enter_finish.set()


async def process_mailer_image_finish(message: types.Message, state: FSMContext):

	# unpack
	async with state.proxy() as storage:
		caption = storage.get("admin_mailer_caption")
		photo = storage.get("admin_mailer_image")
		link = storage.get("admin_mailer_link")

	all_users = await orm.get_all_users()

	counter = 0

	await message.answer(
		text = "▶️ Рассылка запущена...",
		reply_markup = get_main_menu_kb()
	)

	await AdminStates.main_menu.set()

	for user in all_users:
		try:
			await g_bot.send_photo(
				chat_id = user.user_id,
				photo = photo,
				caption = caption,
				reply_markup = get_mailer_btn_ikb(link = link) if link is not None else None,
				parse_mode = ParseMode.HTML
			)

			counter += 1
		except:
			pass

	await message.answer(
		text = f"✅ Рассылка завершена! Сообщение отправлено {counter}/{len(all_users)}."
	)