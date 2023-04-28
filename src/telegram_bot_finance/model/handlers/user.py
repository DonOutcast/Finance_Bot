from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from model.template.templates import render

from model.services.categories import Categories


user_router = Router()
headers = {"throttling_key": "default", "long_operation": "typing"}

@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer(text="Hello start")
    await message.answer(text=render.render_template(template_name="user.html"))


@user_router.message(Command(commands="categories"), flags=headers)
async def show_list_categories(message: Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    await message.answer(text=render.render_template("category.html", {"categories": categories}))
