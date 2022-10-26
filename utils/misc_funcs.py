import ast
import humanize

from loader import bot

from aiogram import exceptions, types
from aiogram.utils.markdown import quote_html

from utils.db.sqliter import get_free_sql

""" Различные функции """

_t = humanize.i18n.activate("ru_RU")
humanize = humanize


def to_fixed(numObj, digits=2) -> str:
    """ Возвращает любое число с плавающей запятой в красивом виде """
    return f"{numObj:.{digits}f}"


async def get_user_data(uid: int, telegram_user: types.User = None, user_data: dict = None, fast_mode=False):
    """ Возвращает юзер дату """
    if not telegram_user and not fast_mode:
        try: telegram_user = await bot.get_chat(uid)
        except Exception as err: return None

    if not user_data and telegram_user:
        user_data = get_free_sql("SELECT * FROM users WHERE uid = %s", (telegram_user.id,))
    elif not user_data and not telegram_user:
        user_data = get_free_sql("SELECT * FROM users WHERE uid = %s", (uid,))

    if user_data is None:
        return None

    if not fast_mode:
        user_data['username'] = quote_html(telegram_user.full_name)
        user_data['telegram_data']: types.User = telegram_user

    user_settings = get_free_sql("SELECT * FROM users_settings WHERE uid = %s", (user_data['uid'],))
    if user_settings is None:
        get_free_sql('INSERT INTO users_settings (uid) VALUES (%s)', (user_data['uid'],))
        user_settings = get_free_sql("SELECT * FROM users_settings WHERE uid = %s", (user_data['uid'],))
    user_data['settings'] = user_settings

    return user_data


async def get_chat_data(chat_id: int, telegram_chat: types.Chat = None):
    """ Возвращает чат дату """
    if not telegram_chat:
        try:
            telegram_chat = await bot.get_chat(chat_id)
        except exceptions.ChatNotFound as err:
            return None
        except Exception as err:
            return None

    if telegram_chat.type == "private":
        return None

    chat_data = get_free_sql('SELECT * FROM chats WHERE chat_id = %s', (telegram_chat.id,))

    if chat_data is None:
        get_free_sql('INSERT INTO chats (chat_id, title) VALUES (%s, %s)',
                     (telegram_chat.id, telegram_chat.title))
        chat_data = get_free_sql('SELECT * FROM chats WHERE chat_id = %s', (telegram_chat.id,))

    if chat_data['title'] != telegram_chat.title:
        get_free_sql('UPDATE chats SET title = %s WHERE chat_id = %s', (telegram_chat.title, telegram_chat.id))
        chat_data['title'] = telegram_chat.title

    chat_data['telegram_data']: types.Chat = telegram_chat

    return chat_data


def get_list_from_string(data: str):
    try:
        ev = ast.literal_eval(data)
        return ev
    except ValueError:
        corrected = "\'" + data + "\'"
        ev = ast.literal_eval(corrected)
        return ev
