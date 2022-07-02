from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import Message


async def help_handler(message: Message):
    text = (f"Hello, {message.from_user.first_name}! 👾\n"
            f"I can analyze text and show you: \n\n"
            f"• How many symbols, words and punctuations are in the text; \n\n"
            f"• Found palindromes in the text; \n\n"
            f"• The most frequent words in the text; \n\n"
            f"• The detected languages of the text; \n\n"
            f"Just <u>write</u> me something!")
    await message.answer(text)


def register_help(dp: Dispatcher):
    dp.register_message_handler(help_handler, CommandHelp())
