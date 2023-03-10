from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State
from aiogram.types import Message

from model.filters.admin import AdminFilter
from model.templates import RenderTemplate

render = RenderTemplate()

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    print("im admin command")
    await message.reply("Доп права!")
