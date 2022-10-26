from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text


@dp.message_handler(content_types="web_app_data")
async def answer(webappinfo: types.WebAppInfo):
    print(webappinfo)


@dp.message_handler(Text(startswith=['вебапп'], ignore_case=True))
@dp.message_handler(commands=['webapp'])
async def cmd_webapp(message: types.Message, user_data: dict):
    text, kb = await get_webapp_text(user_data)
    await message.reply(text, reply_markup=kb)


async def get_webapp_text(user_data: dict):
    text = 'https://vistate.x-net.pp.ua/game.html'
    kb = types.InlineKeyboardMarkup()
    # kb.insert(types.InlineKeyboardButton('Закрыть', callback_data='close'))
    kb.insert(types.InlineKeyboardButton(
        'Vistate Online', web_app=types.WebAppInfo(url='https://vistate.x-net.pp.ua/game.html')
    ))
    return text, kb
