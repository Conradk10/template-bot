from loader import dp
from aiogram import types


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, user_data: dict):
    text, kb = await get_start_text(user_data)
    await message.reply(text, reply_markup=kb)


async def get_start_text(user_data: dict):
    text = 'Start text'
    kb = types.InlineKeyboardMarkup()
    kb.insert(types.InlineKeyboardButton('Закрыть', callback_data='close'))
    return text, kb
