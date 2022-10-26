from loader import dp
from aiogram import types
from utils import get_free_sql
from handlers.user.registration import cmd_register


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, user_data: dict):
    text, kb = await get_start_text(user_data)
    if text is None:
        await cmd_register(message, user_data)
        return
    await message.reply(text, reply_markup=kb)


async def get_start_text(user_data: dict):
    _ = get_free_sql("SELECT * FROM settings WHERE setting = %s", ('registration_available',))
    if _['int_value']:  # Если регистрация разрешена
        return None, None
    text = 'Сейчас регистрация закрыта'
    kb = types.InlineKeyboardMarkup()
    # kb.insert(types.InlineKeyboardButton('Закрыть', callback_data='close'))
    return text, kb
