from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from model.template.templates import render


user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer(text="Hello start")
    await message.answer(text=render.render_template(template_name="user.html"))
