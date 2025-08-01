# sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BIGINT, VARCHAR, Boolean, DateTime, SmallInteger, ARRAY, DOUBLE_PRECISION, JSON


# init baseModel
BaseModel = declarative_base()


class User(BaseModel):

	__tablename__ = "users"

	# base
	user_id = Column(BIGINT, primary_key = True, nullable = False)
	username = Column(VARCHAR(33), nullable = False)
	fullname = Column(VARCHAR(128), nullable = False)
	register_date = Column(DateTime, nullable = False)
	inventory = Column(ARRAY(Integer), nullable = False, default = [])
	points = Column(BIGINT, nullable = False, default = 0)
	season_points = Column(BIGINT, nullable = False, default = 0)
	attempts = Column(Integer, nullable = False, default = 1)
	upd_date = Column(DateTime, nullable = True)
	freeze = Column(Integer, nullable = False, default = 0)
	promocodes = Column(ARRAY(String), nullable = False, default = [])

	# jumanji
	jumanji_attempts = Column(JSON, nullable = False, default = {"dice": 1, "freecard": 1, "box": 1, "casino": 1, "basket": 1, "darts": 1, "bowling": 1})


class Card(BaseModel):

	__tablename__ = "cards"

	card_id = Column(Integer, autoincrement = True, primary_key = True)
	card_name = Column(String, nullable = False)
	card_image = Column(String, nullable = False)
	card_weight = Column(Integer, nullable = False)
	card_rarity = Column(String, nullable = False)
	card_target = Column(String, nullable = False)


class Transaction(BaseModel):

	__tablename__ = "transactions"

	transaction_id = Column(Integer, autoincrement = True, primary_key = True)
	transaction_user_id = Column(BIGINT, nullable = False)
	transaction_type = Column(String, nullable = False) # ex: get_card, transfer, jumanji_dice
	transaction_date = Column(DateTime, nullable = False) # utc
	transaction_in = Column(ARRAY(String), nullable = False, default = [])
	transaction_out = Column(ARRAY(String), nullable = False, default = [])


class Promocode(BaseModel):

	__tablename__ = "promocodes"

	promocode_id = Column(Integer, autoincrement = True, primary_key = True)
	promocode_name = Column(String, nullable = False)
	promocode_usages = Column(Integer, nullable = False)
	promocode_value = Column(ARRAY(String), nullable = False)
