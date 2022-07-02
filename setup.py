from aiogram import Dispatcher

from tgbot.handlers.analyze import register_analyze_text
from tgbot.handlers.help import register_help
from tgbot.handlers.start import register_start


def register_all_handlers(dp: Dispatcher):
    register_start(dp)
    register_help(dp)
    register_analyze_text(dp)
