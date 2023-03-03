import asyncio
from model.templates import render_template
from aiogram.filters.command import Command
from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from configurate.config import TELEGRAM_BOT_TOKEN

bot = Bot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage
dp = Dispatcher()
dp.message.filter(F.chat.type == "private")


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await bot.send_message(message.from_user.id, text=render_template("help.j2"))


async def main():
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()





if __name__ == "__main__":
    asyncio.run(main())
