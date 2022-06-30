import logging

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, ChatNotFound


async def on_startup_notify(bot: Bot):
    config = bot.get('config')
    for admin in config.tg_bot.admin_ids:
        try:
            await bot.send_message(admin, "The bot is ready on the branch master")
        except BotBlocked:
            logging.warning("Forbidden: bot was blocked by the user")
        except ChatNotFound:
            logging.warning("Forbidden: Chat not found")

