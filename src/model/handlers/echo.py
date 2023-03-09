from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
from src.model.templates import RenderTemplate

render = RenderTemplate()
echo_router = Router()


@echo_router.message(F.text)
async def bot_echo(message: types.Message):
    await message.answer(text=render.render_template("echo.html", {"message": message.text}))
    # await message.answer(text=render_template("echo.html", {"message": message.text}))


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Эхо у состояние {hcode(state_name)}',
        'Содержание сообщения:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))
