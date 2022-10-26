import datetime

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils import get_user_data, dialogs, get_free_sql


class UserDataMiddleware(BaseMiddleware):
    def __init__(self, key_prefix='userdata_'):
        self.prefix = key_prefix
        super(UserDataMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        user_data = await get_user_data(message.from_user.id, message.from_user)

        if user_data is None:
            text, kb = dialogs.user_not_registred_dialog()
            await message.reply(text, reply_markup=kb)
            raise CancelHandler()   # TODO: Изменить диалог

        if user_data['uid'] == message.from_user.id:
            now = datetime.datetime.now()
            get_free_sql('UPDATE users SET last_action = %s WHERE uid = %s',
                         (now, user_data['uid']))
            user_data['last_action'] = now

        data['user_data'] = user_data

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user_data = await get_user_data(callback_query.from_user.id, callback_query.from_user)

        if user_data['uid'] == callback_query.from_user.id:
            now = datetime.datetime.now()
            get_free_sql('UPDATE users SET last_action = %s WHERE uid = %s',
                         (now, user_data['uid']))
            user_data['last_action'] = now

        data['user_data'] = user_data
