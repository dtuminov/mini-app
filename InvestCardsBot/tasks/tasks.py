# DB
from database.orm import ORM as orm

# Another
from datetime import datetime, timedelta
import logging, asyncio


async def every_week():
	while True:
		# Get current date and time
		current = datetime.now()

		# Calculate the next Monday
		if current.weekday() == 0:
			next_monday = current + timedelta(days=7)
		else:
			days_ahead = (7 - current.weekday()) % 7
			next_monday = current + timedelta(days=days_ahead)

		# Clear time
		target_day = datetime(
			year=next_monday.year,
			month=next_monday.month,
			day=next_monday.day,
			hour=0,
			minute=0,
			second=0
		)

		# Debug
		logging.info(f"Next week checking in {target_day}")

		# Calculate the cooldown duration
		cooldown = (target_day - current).total_seconds()

		# Wait for the next week to start
		await asyncio.sleep(cooldown)

		# get all users
		all_users = await orm.get_all_users()
		
		# initiate 
		jumanji_attempts = {
			"dice": 1,
			"freecard": 1,
			"box": 1,
			"casino": 1,
			"basket": 1,
			"darts": 1,
			"bowling": 1
		}

		# set jumanji attempts
		for user in all_users:
			await orm.set_users_field(user.user_id, "jumanji_attempts", jumanji_attempts)


async def every_hour():
	while True:
		await asyncio.sleep(3600)
		
		# get all users
		all_users = await orm.get_all_users()
		
		# decrement freeze hours
		for user in all_users:
			if user.freeze > 0:
				await orm.set_users_field(user.user_id, "freeze", user.freeze - 1)


async def change_season():
	while True:
		# Get current date and time
		current = datetime.now()

		# Calculate the next month's first day
		if current.month == 12:
			nextmonth = current.replace(year=current.year + 1, month=1, day=1)
		else:
			nextmonth = current.replace(month=current.month + 1, day=1)

		# Clear time
		targetday = datetime(
			year = nextmonth.year,
			month = nextmonth.month,
			day = nextmonth.day,
			hour = 0,
			minute = 0,
			second = 0
		)

		# Debug
		logging.info(f"Next month checking in {targetday}")

		# Calculate the cooldown duration
		cooldown = (targetday - current).total_seconds()

		# Wait for the next month to start
		await asyncio.sleep(cooldown)

		all_users = await orm.get_all_users()

		for user in all_users:
			await orm.set_users_field(user.user_id, "season_points", 0)
