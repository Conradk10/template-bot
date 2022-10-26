from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils import get_user_data


class UserDataMiddleware(BaseMiddleware):
    def __init__(self, key_prefix='userdata_'):
        self.prefix = key_prefix
        super(UserDataMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_data = await get_user_data(message.from_user.id, message.from_user)
        data['user_data'] = user_data

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_data = await get_user_data(callback_query.from_user.id, callback_query.from_user)
        data['user_data'] = user_data
