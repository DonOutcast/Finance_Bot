from typing import List

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


class SetCommands:

    def __init__(self, bot: Bot):
        self.bot = Bot
        self.commands = await self.bot.get_my_commands()

    async def _default_commands(self):
        """Set of commands with description"""
        await self.bot.set_my_commands([
            BotCommand(command="start", description="Старт"),
            BotCommand(command="help", description="Помощь"),
            BotCommand(command="del", description="Удаление одной записи"),
            BotCommand(command="categories", description="Категории"),
            BotCommand(command="today", description="Сегодня"),
            BotCommand(command="month", description="Месячные"),
            BotCommand(command="expenes", description="Последние")
        ], scope=BotCommandScopeDefault())

    async def get_information_commands(self) -> list[BotCommand]:
        return self.commands

    async def set_default_commands(self):
        if self.commands:
            await self.bot.delete_my_commands()
        await self.set_default_commands()
