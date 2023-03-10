from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from model.templates import RenderTemplate

render = RenderTemplate()
user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer(text="Hello start")
    await message.answer(text=render.render_template(template_name="user.html"))
    print(type(message.from_user.id), message.from_user.id)