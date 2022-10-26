import traceback
from aiogram import types
from aiogram.utils.markdown import quote_html
import data.config
from loader import dp, bot
from aiogram.types import ParseMode
from meval import meval


async def getattrs(message, user_data):
    return {
        "user_data": user_data,
        "reply": message.reply_to_message,
        "chat_id": message.chat.id,
        "message": message,
        "bot": bot,
        "dp": dp
    }


@dp.message_handler(lambda message: message.from_user.id in data.config.admins, commands=['eval'])
async def cmd_eval(message: types.Message):
    user_data = {}
    args = message.get_args()
    try:
        output = await meval(args, globals(), **await getattrs(message, user_data))
    except Exception:
        error = traceback.format_exc(limit=0, chain=True)
        return await message.reply(
            ("<b>Ошибка:</b>\n"
             f"<code>{quote_html(error)}</code>"),
            parse_mode=ParseMode.HTML
        )
    else:
        return await message.reply(
            ("<b>Выполненное выражение:</b>\n"
             f"<code>{quote_html(args)}</code>\n"
             "<b>Возвращено:</b>\n"
             f"<code>{quote_html(output)}</code>"),
            parse_mode=ParseMode.HTML
        )


@dp.message_handler(lambda message: message.from_user.id in data.config.admins, commands=['exec'])
async def cmd_exec(message: types.Message, user_data: dict):
    args = message.get_args()
    try:
        output = await meval(args, globals(), **await getattrs(message, user_data))
    except Exception:
        error = traceback.format_exc(limit=0, chain=True)
        return await message.reply(
            ("<b>Ошибка:</b>\n"
             f"<code>{quote_html(error)}</code>"),
            parse_mode=ParseMode.HTML
        )
