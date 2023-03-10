from aiogram.filters import BaseFilter
from aiogram.types import Message

from configurate import config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    async def __call__(self, obj: Message, config: config) -> bool:
        print("sdfs")
        return (obj.from_user.id in config.admins) == self.is_admin