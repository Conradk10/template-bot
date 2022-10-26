from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins


class InProgressFilter(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in admins:
            return False
        return True
