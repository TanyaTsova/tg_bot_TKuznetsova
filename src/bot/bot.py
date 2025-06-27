import asyncio

from aiogram import Bot, Dispatcher, html, types
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings.config import config
from src.bot import commands, quiz

dp = Dispatcher()

dp.include_router(commands.router)
dp.include_router(quiz.router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message_handler(commands=["help"])  # /help
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def main() -> None:
    bot = Bot(token=config.pa)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
