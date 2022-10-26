from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivateFilter(BoundFilter):
    async def check(self, message: types.Message):
        if message.chat.type != 'private':
            text = '<b>Ошибка</b>:\n' \
                   '└  <i>Данная команда работает только в личных сообщениях!</i>'
            kb = types.InlineKeyboardMarkup(row_width=1)
            kb.insert(types.InlineKeyboardButton('Перейти в личные сообщения',
                                                 url='https://t.me/vistatebot'))
            # kb.insert(types.InlineKeyboardButton('Закрыть', callback_data='close'))
            await message.answer(text, reply_markup=kb)
            return False
        return True
