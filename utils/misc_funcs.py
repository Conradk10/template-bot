import ast
import math
import hashlib
import humanize

from loader import bot

from aiogram import exceptions, types
from aiogram.utils.markdown import quote_html

from utils.vars import levels_data
from utils.db.sqliter import get_free_sql

""" Различные функции """

_t = humanize.i18n.activate("ru_RU")
humanize = humanize


def to_fixed(numObj, digits=2) -> str:
    """ Возвращает любое число с плавающей запятой в красивом виде """
    return f"{numObj:.{digits}f}"


async def get_user_token(uid: int) -> str:
    """ Возвращает md5 токен юзера """
    md5_key = 'vistate'
    return hashlib.md5(str(f'{md5_key}+{uid}').strip().encode()).hexdigest()


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

    user_data['fullname'] = ' '.join([user_data['name'], user_data['surname']])
    next_level_data = get_free_sql('SELECT * FROM levels WHERE level = %s', (user_data['level'] + 1,))
    curr_level_data = get_free_sql('SELECT * FROM levels WHERE level = %s', (user_data['level'],))
    user_data['curr_respect'] = user_data['respect'] - curr_level_data['exp']
    user_data['next_respect'] = next_level_data['exp'] - curr_level_data['exp']

    if not fast_mode:
        user_data['username'] = quote_html(telegram_user.full_name)
        user_data['telegram_data']: types.User = telegram_user

    user_settings = get_free_sql("SELECT * FROM users_settings WHERE uid = %s", (user_data['uid'],))
    if user_settings is None:
        get_free_sql('INSERT INTO users_settings (uid) VALUES (%s)', (user_data['uid'],))
        user_settings = get_free_sql("SELECT * FROM users_settings WHERE uid = %s", (user_data['uid'],))

    user_data['settings'] = user_settings

    user_items = get_free_sql("SELECT * FROM users_items WHERE owner = %s", (user_data['uid'],), fetchall=True)
    user_vehicles = []
    for user_item in user_items:
        if user_item['type'].startswith('veh:'):
            user_vehicles.append(user_item)
    user_data['user_vehicles'] = user_vehicles

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


def fill_levels_exp() -> None:
    """ Заполняет уровни в БД """
    last_exp = 4
    last_total = 0
    for i in range(260):
        last_total = last_exp + last_total + 4
        last_exp += 4
        level = i + 2
        exp = last_total
        if 0 <= level <= 255:
            get_free_sql("update levels set exp = %s where level = %s", (exp, level))


def get_online_users(online_seconds: int = 300) -> list:
    """ Возвращает список игроков онлайн в течении прошедших online_seconds """
    return [_['uid'] for _ in get_free_sql(
        'SELECT uid FROM users WHERE last_action > current_timestamp() - %s',
        (online_seconds, ),
        fetchall=True
    )]


async def update_user_respect(uid: int, user_data: dict = None, respect_amount=0):
    """ Увеличить респекты игрока на respect_amount ед. """
    if user_data is None:
        user_data = get_free_sql("SELECT level, respect FROM users WHERE uid = %s", (uid,))
    # Увеличивать уровень игроку пока его опыт не будет меньше чем опыт следующего уровня
    new_respect = user_data['respect'] + respect_amount
    user_level = user_data['level']
    db_level_data = next((sub for sub in levels_data if sub['level'] == user_level + 1), None)
    while new_respect >= db_level_data['exp']:
        user_level += 1
        db_level_data = next((sub for sub in levels_data if sub['level'] == user_level + 1), None)
    if respect_amount or user_data['level'] != user_level:
        get_free_sql("UPDATE users SET respect = %s, level = %s WHERE uid = %s",
                     (new_respect, user_level, user_data['uid']))
        user_data['level'] = user_level
        user_data['respect'] = new_respect
    return user_data


def get_list_from_string(data: str):
    try:
        ev = ast.literal_eval(data)
        return ev
    except ValueError:
        corrected = "\'" + data + "\'"
        ev = ast.literal_eval(corrected)
        return ev


def get_distanse_between_coords(x_pos1, y_pos1, x_pos2, y_pos2):
    _ = math.sqrt(((x_pos1 - x_pos2) ** 2) + ((y_pos1 - y_pos2) ** 2))
    return _


def get_all_locations(user_data: dict, page=None):
    if page:
        _ = get_free_sql("SELECT * FROM locations LIMIT %s,6", ((page-1)*6,), fetchall=True)
    else:
        _ = get_free_sql("SELECT * FROM locations", fetchall=True)
    for location_data in _:
        location_data['distance_to_user'] = round(get_distanse_between_coords(
            user_data['x_pos'], user_data['y_pos'],
            location_data['x_pos'], location_data['y_pos']
        ) * 2)
    locations_count = (get_free_sql("SELECT COUNT(id) FROM locations"))["COUNT(id)"]
    return _, locations_count


def get_all_locations_sql(user_data: dict):
    _ = get_free_sql(
        "SELECT *, SQRT(((x_pos - %s) ^ 2) + ((y_pos - %s) ^ 2)) AS 'distance_to_user' "
        "FROM locations WHERE SQRT(((x_pos - 1) * 2) + ((y_pos - 1) * 2)) < 90;",
        (user_data['x_pos'], user_data['y_pos'])
    )
    return _
