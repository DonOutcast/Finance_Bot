from aiogram import Bot
from aiogram import Dispatcher
from aiogram import exceptions
from aiogram.fsm.storage.memory import MemoryStorage

from configurate.config import settings

from model.handlers.user import user_router
from model.handlers.echo import echo_router
from model.handlers.admin import admin_router

from model.middlewares.config import ConfigMiddleware
from model.middlewares.throttling import ThrottlingMiddelware
from model.middlewares.chataction import ChatActionMiddleware

from model.services import broadcaster


# from model.handlers.echo import echo_router
class Singleton(object):
    __instance = None
    bot = Bot(settings.bot_token.get_secret_value(), parse_mode="HTML")
    storage = MemoryStorage
    dp = Dispatcher()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True

    def _register_global_middlewares(self, config: settings):
        self.dp.message.middleware(ChatActionMiddleware())
        self.dp.message.outer_middleware(ConfigMiddleware(config))

    async def _on_startup(self, admin_ids: list[int]):
        await broadcaster.broadcast(self.bot, admin_ids, "Бот запущен!")

    async def main(self):
        for router in [admin_router, user_router, echo_router]:
            self.dp.include_router(router)
        self._register_global_middlewares(settings)
        try:
            print("run!")
            await self._on_startup(settings.admins)
            await self.bot.delete_webhook(drop_pending_updates=True)
            await self.dp.start_polling(self.bot, allowed_updates=self.dp.resolve_used_update_types())
        except exceptions as ex:
            print(ex)
        finally:
            await self.bot.session.close()
