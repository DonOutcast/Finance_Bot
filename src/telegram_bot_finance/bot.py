import asyncio
from model.handlers.echo import echo_router
from model.handlers.admin import admin_router
from model.handlers.user import user_router
# from model.templates import render_template
from configurate.config import settings, Settings
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import exceptions
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeAllGroupChats
from aiogram.exceptions import TelegramAPIError

from model.middlewares.config import ConfigMiddleware
from model.middlewares.chataction import ChatActionMiddleware
from model.services import broadcaster

bot = Bot(settings.bot_token.get_secret_value(), parse_mode="HTML")
storage = MemoryStorage


# bot = bot.get_current()



# @user_router.message(Command("start"))
# @debugorator(config.debug)
# async def cmd_start(message: Message):
#     await bot.send_message(message.from_user.id, text="Команда '/start'")
#
#
# @user_router.message(Command("help"))
# async def cmd_help(message: Message):
#     await bot.send_message(message.from_user.id, text=render.render_template("index.html"))


# @r.message(Command("help"))
# async def cmd_help(message: Message):
#     await bot.send_message(chat_id=1134902789, text="Оставь да")

def register_global_middlewares(dp: Dispatcher, settings: Settings) -> None:
    dp.message.outer_middleware(ConfigMiddleware(settings))
    # dp.message.outer_middleware(ThrottlingMiddelware())
    dp.message.middleware(ChatActionMiddleware())


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен!")


async def main():
    dp = Dispatcher()
    # dp.message.filter(F.chat.type == "private")
    for router in [admin_router, user_router, echo_router]:
        dp.include_router(router)
    register_global_middlewares(dp, settings)
    await set_default_commands(bot)
    try:
        # await bot.send_message(chat_id=1134902789, text="Оставь да", disable_notification=False)
        await on_startup(bot, settings.admins)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except exceptions as ex:
        print(ex)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
# import asyncio
# import logging
# import sys
# from os import getenv
# from typing import Any, Dict
#
# from aiogram import Bot, Dispatcher, F, Router, html
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import (
#     KeyboardButton,
#     Message,
#     ReplyKeyboardMarkup,
#     ReplyKeyboardRemove,
# )
#
# form_router = Router()
#
#
# class Form(StatesGroup):
#     name = State()
#     like_bots = State()
#     language = State()
#
#
# @form_router.message(Command("start"))
# async def command_start(message: Message, state: FSMContext) -> None:
#     await state.set_state(Form.name)
#     await message.answer(
#         "Hi there! What's your name?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#
# @form_router.message(Command("cancel"))
# @form_router.message(F.text.casefold() == "cancel")
# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     logging.info("Cancelling state %r", current_state)
#     await state.clear()
#     await message.answer(
#         "Cancelled.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#
# @form_router.message(Form.name)
# async def process_name(message: Message, state: FSMContext) -> None:
#     await state.update_data(name=message.text)
#     await state.set_state(Form.like_bots)
#     await message.answer(
#         f"Nice to meet you, {html.quote(message.text)}!\nDid you like to write bots?",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[
#                 [
#                     KeyboardButton(text="Yes"),
#                     KeyboardButton(text="No"),
#                 ]
#             ],
#             resize_keyboard=True,
#         ),
#     )
#
#
# @form_router.message(Form.like_bots, F.text.casefold() == "no")
# async def process_dont_like_write_bots(message: Message, state: FSMContext) -> None:
#     data = await state.get_data()
#     await state.clear()
#     await message.answer(
#         "Not bad not terrible.\nSee you soon.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     await show_summary(message=message, data=data, positive=False)
#
#
# @form_router.message(Form.like_bots, F.text.casefold() == "yes")
# async def process_like_write_bots(message: Message, state: FSMContext) -> None:
#     await state.set_state(Form.language)
#
#     await message.reply(
#         "Cool! I'm too!\nWhat programming language did you use for it?",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#
# @form_router.message(Form.like_bots)
# async def process_unknown_write_bots(message: Message, state: FSMContext) -> None:
#     await message.reply("I don't understand you :(")
#
#
# @form_router.message(Form.language)
# async def process_language(message: Message, state: FSMContext) -> None:
#     data = await state.update_data(language=message.text)
#     await state.clear()
#     text = (
#         "Thank for all! Python is in my hearth!\nSee you soon."
#         if message.text.casefold() == "python"
#         else "Thank for information!\nSee you soon."
#     )
#     await message.answer(text)
#     await show_summary(message=message, data=data)
#
#
# async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
#     name = data["name"]
#     language = data.get("language", "<something unexpected>")
#     text = f"I'll keep in mind that, {html.quote(name)}, "
#     text += (
#         f"you like to write bots with {html.quote(language)}."
#         if positive
#         else "you don't like to write bots, so sad..."
#     )
#     await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
#
#
# async def main():
#     bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
#     dp = Dispatcher()
#     for router in [form_router, echo_router]:
#         dp.include_router(router)
#
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())
