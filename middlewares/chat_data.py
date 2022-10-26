from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils import get_chat_data


class ChatDataMiddleware(BaseMiddleware):
    def __init__(self, key_prefix='chatdata_'):
        self.prefix = key_prefix
        super(ChatDataMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        chat_data = await get_chat_data(message.chat.id, message.chat)
        data['chat_data'] = chat_data

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        chat_data = await get_chat_data(callback_query.message.chat.id, callback_query.message.chat)
        data['chat_data'] = chat_data
