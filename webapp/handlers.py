import json
from datetime import datetime

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response

from data import config
from utils.web_app import safe_parse_webapp_init_data
from utils import get_list_from_string, get_user_data

SEND_MESSAGE_DELTA = {}
CHECK_DATA_DELTA = {}


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


app = web.Application()
app.add_routes([web.post('/webapp/checkUserData', web_check_user_data),])
