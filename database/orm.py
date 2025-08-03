# sqlalchemy import
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

# Database engine
from database.engine import create_async_engine, get_session_maker

# DB Models
from database.db_models import *

# My modules
from modules.cfg_loader import load_config

# Another
from datetime import datetime, timedelta
from copy import deepcopy


# Load cfg
db_config = load_config("cfg/db_config.json")

# create engine
async_engine = create_async_engine(
	url = f"postgresql+asyncpg://{db_config.get('user')}:{db_config.get('password')}@{db_config.get('host')}:5432/{db_config.get('database')}"
)

# create session_maker
session_maker = get_session_maker(async_engine)


class ORM:

	@staticmethod
	async def proceed_schemas() -> None:
		async with async_engine.begin() as conn:
			await conn.run_sync(BaseModel.metadata.create_all)


	### USERS MANAGEMENT
	@staticmethod
	async def is_user_exists(user_id: int) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(User.user_id).where(User.user_id == user_id))

				if query.one_or_none() is None:
					return False
				else:
					return True
				

	@staticmethod
	async def is_user_exists_username(username: str) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(User.user_id).where(User.username == username))

				if query.one_or_none() is None:
					return False
				else:
					return True


	@staticmethod
	async def create_user_if_not_exists(user_id: int, username: str, fullname: str, register_date: datetime) -> None:
		async with session_maker() as session:
			async with session.begin():
				if not await ORM.is_user_exists(user_id):
					user = User(
						user_id = user_id,
						username = username,
						fullname = fullname,
						register_date = register_date,
						upd_date = register_date
					)
					
					await session.merge(user)

					return True
				else:
					return False


	@staticmethod
	async def set_users_field(user_id: int, field: str, value: int|str|bool) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(update(User).where(User.user_id == user_id).values({getattr(User, field): value}))
	

	@staticmethod
	async def get_user(user_id: int) -> User:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.user_id == user_id))

				return query.one_or_none()
			
	
	@staticmethod
	async def get_user_byUsername(username: str) -> User:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.username == username))

				return query.one_or_none()
			
	
	@staticmethod
	async def get_referrals(referrer_id: int) -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.referrer_id == referrer_id))

				return query.all()
			

	@staticmethod
	async def get_all_users() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User))

				return query.all()
			
		
	@staticmethod
	async def get_all_streamPass_users() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.stream_pass != 0))

				return query.all()
			
	
	@staticmethod
	async def get_inventory(user_id: int) -> User:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User.inventory).where(User.user_id == user_id))

				return query.one_or_none()


	@staticmethod
	async def get_squad_users(squad_id: int) -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.squad_id == squad_id))

				return query.all()


	@staticmethod
	async def get_active_users_byToday() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(User).where(User.upd_date >= datetime.now().date()))

				return query.all()
			

	@staticmethod
	async def get_active_users_byWeek() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				now = datetime.now()
				days_since_monday = now.weekday()

				pn = now - timedelta(days = days_since_monday)
				pn = pn.replace(hour=0, minute=0, second=0, microsecond=0)

				query = await session.scalars(select(User).where(User.upd_date >= pn))

				return query.all()
			

	@staticmethod
	async def get_active_users_byMonth() -> list[User]:
		async with session_maker() as session:
			async with session.begin():
				now = datetime.now()
				first_month_day = now.replace(day = 1, hour=0, minute=0, second=0, microsecond=0)

				query = await session.scalars(select(User).where(User.upd_date >= first_month_day))

				return query.all()
	### CARDS
	@staticmethod
	async def is_card_exists(card_id: int) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Card.card_id).where(Card.card_id == card_id))

				if query.one_or_none() is None:
					return False
				else:
					return True

	@staticmethod
	async def create_card(card_name: str, card_image: str, card_weight: int, card_rarity: str, card_target: str) -> None:
		async with session_maker() as session:
			async with session.begin():
				card = Card(
					card_name = card_name,
					card_image = card_image,
					card_weight = card_weight,
					card_rarity = card_rarity,
					card_target = card_target
				)
				
				await session.merge(card)


	@staticmethod
	async def update_card(card_id: int, card_name: str, card_image: str, card_weight: int, card_rarity: str, card_target: str) -> None:
		async with session_maker() as session:
			async with session.begin():
				card_data = {
					"card_name": card_name,
					"card_image": card_image,
					"card_weight": card_weight,
					"card_rarity": card_rarity,
					"card_target": card_target
				}

				await session.execute(update(Card).where(Card.card_id == card_id).values(card_data))


	@staticmethod
	async def get_cards_by_rarity_for_drop(rarity: str) -> list[Card]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Card).where(Card.card_rarity == rarity, Card.card_target == "drop"))

				return query.all()
			

	@staticmethod
	async def get_legendary_cards_for_craft() -> list[Card]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Card.card_id).where(Card.card_target == "drop", Card.card_rarity == "ultraRare"))

				return query.all()


	@staticmethod
	async def get_cards_by_rarity(rarity: str) -> list[Card]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Card).where(Card.card_rarity == rarity))

				return query.all()
			
	
	@staticmethod
	async def get_cards_ids_by_rarity(rarity: str) -> list[Card]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Card.card_id).where(Card.card_rarity == rarity))

				return query.all()
			
	
	@staticmethod
	async def get_card_by_cardID(card_id: int) -> Card:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Card).where(Card.card_id == card_id))

				return query.one_or_none()
			

	### TRANSACTIONS
	@staticmethod
	async def create_transaction(transaction_user_id: int, transaction_type: str, transaction_date: datetime, transaction_in: list[str] = [], transaction_out: list[str] = []) -> None:
		async with session_maker() as session:
			async with session.begin():
				transaction = Transaction(
					transaction_user_id = transaction_user_id,
					transaction_type = transaction_type,
					transaction_date = transaction_date,
					transaction_in = transaction_in,
					transaction_out = transaction_out
				)
				
				await session.merge(transaction)


	@staticmethod
	async def get_user_transactions(user_id: int) -> list[Transaction]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Transaction).where(Transaction.transaction_user_id == user_id))

				return query.all()
			
	
	### PROMO
	@staticmethod
	async def is_promo_exists(promocode_id: int) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Promocode).where(Promocode.promocode_id == promocode_id))

				return query.one_or_none() is not None


	@staticmethod
	async def is_promo_exists_by_name(promocode_name: str) -> bool:
		async with session_maker() as session:
			async with session.begin():
				query = await session.execute(select(Promocode).where(Promocode.promocode_name == promocode_name))

				return query.one_or_none() is not None


	@staticmethod
	async def create_promo(promocode_name: str, promocode_usages: int, promocode_value: list[str]) -> None:
		async with session_maker() as session:
			async with session.begin():
				promocode = Promocode(
					promocode_name = promocode_name,
					promocode_usages = promocode_usages,
					promocode_value = promocode_value
				)
				
				await session.merge(promocode)


	@staticmethod
	async def delete_promo(promocode_id: int) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(delete(Promocode).where(Promocode.promocode_id == promocode_id))


	@staticmethod
	async def get_all_promo() -> list[Promocode]:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Promocode))

				return query.all()
			

	@staticmethod
	async def get_promo_by_name(promocode_name: str) -> Promocode:
		async with session_maker() as session:
			async with session.begin():
				query = await session.scalars(select(Promocode).where(Promocode.promocode_name == promocode_name))

				return query.one_or_none()
			

	@staticmethod
	async def decrement_promo_usages(promocode_name: str, decrementator: int = 1) -> None:
		async with session_maker() as session:
			async with session.begin():
				await session.execute(update(Promocode).where(Promocode.promocode_name == promocode_name).values(promocode_usages = Promocode.promocode_usages - decrementator))


	