# mini-app — InvestCardsBot

Telegram bot (aiogram, Redis-backed FSM) distributing gamified "investment
cards" to users: `get_card`, `my_cards`, and `stream_place` handlers drive
card drops and a leaderboard-style placement mechanic. Deployment notes for
nginx/certbot are in `setup_nginx.txt`/`setup_certbot.txt`.
