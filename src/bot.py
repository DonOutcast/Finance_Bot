# import asyncio
# # from model.templates import render_template
# from configurate.config import config
# from model.templates import RenderTemplate
# from aiogram.filters.command import Command
# from aiogram import Bot, Dispatcher, F
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message
# from configurate.config import TELEGRAM_BOT_TOKEN
#
#
# render = RenderTemplate()
# print("This conf", config)
# bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
# storage = MemoryStorage
# dp = Dispatcher()
# dp.message.filter(F.chat.type == "private")
#
#
# @dp.message(Command("start"))
# async def cmd_start(message: Message):
#     await bot.send_message(message.from_user.id, text=message.json())
#
#
# @dp.message(Command("help"))
# async def cmd_help(message: Message):
#     await bot.send_message(message.from_user.id, text=render.render_template("index.html"))
#
#
# async def main():
#     try:
#         await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#     finally:
#         await bot.session.close()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
