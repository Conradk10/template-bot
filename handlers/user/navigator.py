import math

from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Text
from utils import get_all_locations, get_free_sql, get_distanse_between_coords, humanize


@dp.message_handler(Text(startswith=['навигатор'], ignore_case=True))
@dp.message_handler(commands=['gps'])
async def cmd_gps(message: types.Message, user_data: dict):
    text, kb = await get_gps_text(user_data)
    await message.reply(text, reply_markup=kb)


async def get_gps_text(user_data: dict):
    locations_data, locations_count = get_all_locations(user_data)
    near_locations = []
    for location_data in locations_data:
        if location_data['distance_to_user'] < 100:
            near_locations.append(
                f"{location_data['title'].lower()} ({round(location_data['distance_to_user'])} м)"
            )
    text = '🧭 ► <b>Навигатор</b>\n\n' \
           f'<b>Всего мест</b>: <code>{locations_count}</code>\n' \
           f'<b>Места поблизости</b>: {", ".join(near_locations) if near_locations else "ничего"}'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f'Места поблизости ({len(near_locations)})',
                                      callback_data='gps m:np'))
    kb.add(types.InlineKeyboardButton(f'Важные места',
                                      callback_data='gps m:ip'))
    kb.add(types.InlineKeyboardButton(f'Обновить',
                                      callback_data='gps'))
    return text, kb


async def get_locations_list_text(user_data: dict, page: int):
    locations_data, locations_count = get_all_locations(user_data, page)
    text = '🧭 ► <b>Навигатор</b>\n\n' \
           f'<b>Всего мест</b>: <code>{locations_count}</code>'

    kb = types.InlineKeyboardMarkup()
    for location in locations_data:
        kb.add(types.InlineKeyboardButton(f'{location["title"]} ({location["distance_to_user"]} м)',
                                          callback_data=f'gps m:li p:{page} id:{location["id"]}'))

    # Пагинация
    max_pages = math.ceil(locations_count / 6)
    if max_pages > 1:
        kb.add(types.InlineKeyboardButton('Пред. стр.' if page > 1 else ' ',
                                          callback_data=f'gps m:ip p:{page - 1}' if page > 1 else 'none'))
        kb.insert(types.InlineKeyboardButton(f'- {page}/{max_pages} -', callback_data=f'none'))
        kb.insert(types.InlineKeyboardButton('След. стр.' if page < max_pages else ' ',
                                             callback_data=f'gps m:ip p:{page + 1}' if page < max_pages else 'none'))
    kb.add(types.InlineKeyboardButton(f'Назад', callback_data='gps'))
    return text, kb


async def get_location_text(user_data: dict, location_id: int, back_to: str, page: int):
    location_data = get_free_sql("SELECT * FROM locations WHERE id = %s", (location_id,))

    location_data['distance_to_user'] = round(get_distanse_between_coords(
        user_data['x_pos'], user_data['y_pos'],
        location_data['x_pos'], location_data['y_pos']
    ) * 2)

    vehicles_info = []
    vehicles_buttons = []
    for vehicle in user_data['user_vehicles']:
        vehicles_info.append(
            f' – <b>{vehicle["title"]}</b>: '
            f'{humanize.naturaldelta(location_data["distance_to_user"] / vehicle["speed"])}\n'
        )
        vehicles_buttons.append(
            types.InlineKeyboardButton(f'Ехать: {vehicle["title"]}',
                                       callback_data=f'gotoloc veh:{vehicle["id"]} id:{location_data["id"]}')
        )

    text = '🧭 ► <b>Навигатор</b>\n\n' \
           f'🚩 <b>{location_data["title"]}</b>\n' \
           f' – <b>Расстояние</b>: <code>{location_data["distance_to_user"]}</code> м\n\n' \
           f'⏳ <b>Время в пути</b>:\n' \
           f' – <b>Пешком</b>: {humanize.naturaldelta(location_data["distance_to_user"] / 1.5)}\n' \
           f'{"".join(vehicles_info)}\n'\
           f'ℹ️ <i>Вы можете вызвать такси через телефон</i>'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(f'Идти: пешком',
                                      callback_data=f'gotoloc veh:0 id:{location_data["id"]}'))
    [kb.add(x) for x in vehicles_buttons]
    kb.add(types.InlineKeyboardButton(f'Назад', callback_data=f'gps m:{back_to} p:{page}'))
    return text, kb


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('gps'))
async def cb_menu(callback_query: types.CallbackQuery, user_data: dict, call_args: dict):
    call_answer = '✅'

    # Места поблизости
    if call_args.get('m') == 'np':
        text, kb = await get_gps_text(user_data)
    # Важные места
    elif call_args.get('m') == 'ip':
        page = int(call_args.get('p', 1))
        text, kb = await get_locations_list_text(user_data, page)
    # Информация о локации
    elif call_args.get('m') == 'li':
        back_to_menu = call_args.get('bt', 'ip')
        page = call_args.get('p', 1)
        location_id = call_args.get('id')
        text, kb = await get_location_text(user_data, location_id, back_to_menu, page)
    # Если ничего не совпало
    else:
        text, kb = await get_gps_text(user_data)

    await callback_query.message.edit_text(text, reply_markup=kb)
    await callback_query.answer(call_answer)
