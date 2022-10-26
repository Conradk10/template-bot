from aiogram import types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.middlewares import BaseMiddleware
from utils.db.sqliter import get_free_sql
from utils.main_funcs import send_logs


class BigBrotherMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='bigbrother_'):
        self.prefix = key_prefix
        super(BigBrotherMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        send_logs(message)

    async def on_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        call_args = {}
        args = callback_query.data.split()
        for arg in args:
            if ':' in arg:
                try:
                    _ = arg.split(':')
                    call_args[_[0]] = _[1]
                except Exception:
                    pass
        data['call_args'] = call_args

    async def on_post_process_callback_query(self, callback_query: types.CallbackQuery, results, data: dict):
        await callback_query.answer(
            f'Ошибка. Callback data кнопки: {callback_query.data}',
            show_alert=True
        )
