from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot.models.user import User


async def start_handler(message: Message, session):
    user_id = message.from_user.id
    user = await session.get(User, user_id)

    if not user:
        config = message.bot.get("config")
        role: str = 'admin' if user_id in config.tg_bot.admin_ids else 'user'
        user = User(
            user_id=user_id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username,
            role=role
        )

        session.add(user)
        await session.commit()

    text = (f"Welcome, {message.from_user.first_name}!\n"
            f"I can analyze any text in any language and show you: \n"
            f"• How many symbols, words and punctuations are in the text; \n\n"
            f"• Found palindromes in the text; \n\n"
            f"• The most frequent words in the text; \n\n"
            f"• The detected languages of the text; \n\n"
            f"Just <u>write</u> me something!")

    await message.answer(text)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_handler, CommandStart())
