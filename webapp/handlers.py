import re
import json
from datetime import datetime
from loader import dp, bot

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from data import config
from handlers.user.registration import get_register_text
from utils.web_app import safe_parse_webapp_init_data
from utils.db.sqliter import get_free_sql
from utils import get_list_from_string, get_user_data

SEND_MESSAGE_DELTA = {}
CHECK_DATA_DELTA = {}
REGISTER_USERNAME_REGEX = r"^(([a-zA-Z'-]{1,80})|([а-яА-ЯЁёІіЇїҐґЄє'-]{1,80}))$"


class DTEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is datetime object
        # convert it to a string
        if isinstance(obj, datetime):
            return obj.timestamp()
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)


async def web_check_user_data(request: Request):
    """ /webapp/checkUserData - проверяет юзера на валидность """
    data = await request.post()

    if not data.get("_auth"):
        return json_response({"ok": False, "error": "Unauthorized"}, status=401)
    data = safe_parse_webapp_init_data(config.BOT_TOKEN, data.get("_auth"))
    r_data = get_list_from_string(str(data.values))["user"]

    user_data = await get_user_data(data["user"]["id"], fast_mode=True)
    json_user_data = json.dumps(user_data, cls=DTEncoder)

    return json_response({"ok": True, "auth": r_data, "user_data": json_user_data}, status=200)


async def web_get_user_data(request: Request):
    """ /webapp/getUserData - возвращает юзер дату"""
    data = await request.post()

    if not data.get("_auth"):
        return json_response({"ok": False, "error": "Unauthorized"}, status=401)
    webapp_data = safe_parse_webapp_init_data(config.BOT_TOKEN, data.get("_auth"))

    request_user_id = data.get("request_user_id", webapp_data["user"]["id"])
    requested_user_data = await get_user_data(request_user_id, fast_mode=True)
    json_user_data = json.dumps(requested_user_data, cls=DTEncoder)

    if not requested_user_data:
        return json_response({"ok": False, "error": "Пользователь не найден"}, status=404)

    return json_response({"ok": True, "user_data": json_user_data}, status=200)


async def web_register_user(request: Request):
    """ /webapp/registerUser - регает юзера """
    data = await request.post()

    if not data.get("_auth"):
        return json_response({"ok": False, "error": "Unauthorized"}, status=401)
    webapp_data = safe_parse_webapp_init_data(config.BOT_TOKEN, data.get("_auth"))

    user_data = await get_user_data(webapp_data["user"]["id"], fast_mode=True)

    if user_data is not None:
        return json_response({"ok": False, "error": "Вы уже проходили регистрацию!"}, status=406)

    if not data.get("_auth"):
        return json_response({"ok": False, "error": "Unauthorized"}, status=401)
    if not data.get("_auth") or not data.get("user_name") or not data.get("user_surname") or not data.get("user_sex"):
        return json_response({"ok": False, "error": "Вы ввели не все данные"}, status=402)
    if data.get("user_sex") not in ["1", "2"]:
        return json_response({"ok": False, "error": "Вы выбрали неверный пол персонажа"}, status=403)
    if re.match(REGISTER_USERNAME_REGEX, data.get("user_name")) is None:
        return json_response({"ok": False, "error": "Вы выбрали неверное имя персонажа"}, status=405)
    if re.match(REGISTER_USERNAME_REGEX, data.get("user_surname")) is None:
        return json_response({"ok": False, "error": "Вы выбрали неверное имя персонажа"}, status=405)

    register_data = {
        "user_name": data.get("user_name"),
        "user_surname": data.get("user_surname"),
        "user_sex": data.get("user_sex")
    }

    get_free_sql("INSERT INTO users (uid, name, surname, sex) VALUES (%s, %s, %s, %s)",
                 (webapp_data["user"]["id"], register_data["user_name"], register_data["user_surname"],
                  "мужской" if register_data["user_sex"] == "1" else "женский"))

    user_data = await get_user_data(webapp_data["user"]["id"], fast_mode=True)
    json_user_data = json.dumps(user_data, cls=DTEncoder)

    json_response({"ok": True, "user_data": json_user_data}, status=200)

    text, kb = await get_register_text(user_data, state=3)
    msg = await bot.send_message(user_data['uid'], text, reply_markup=kb)
    await bot.edit_message_reply_markup(user_data['uid'], msg.message_id-1, reply_markup=None)


app = web.Application()
app.add_routes([web.post('/webapp/checkUserData', web_check_user_data),
                web.post('/webapp/getUserData', web_get_user_data),
                web.post('/webapp/registerUser', web_register_user)])
