from loader import dp
from aiogram import types
from utils import get_online_users
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(startswith=['меню'], ignore_case=True))
@dp.message_handler(commands=['menu'])
async def cmd_menu(message: types.Message, user_data: dict):
    text, kb = await get_menu_text(user_data)
    await message.reply(text, reply_markup=kb)


async def get_menu_text(user_data: dict) -> (str, types.InlineKeyboardMarkup):
    online_users = get_online_users()
    text = f'🖲 ► <b>Главное меню</b>\n\n' \
           f'<b>Игроков онлайн</b>: <code>{len(online_users)}</code>'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Статистика персонажа', callback_data='mm m:st'))
    return text, kb


async def get_menu_statistics_text(user_data: dict) -> (str, types.InlineKeyboardMarkup):
    text = f'📇 ► <b>Статистика персонажа</b>\n\n' \
           f'<b>Имя</b> – {user_data["fullname"]}\n' \
           f'<b>Пол</b> – {user_data["sex"]}\n' \
           f'<b>Уровень</b> – <code>{user_data["level"]}</code>\n' \
           f'<b>Уважение</b> – <code>{user_data["curr_respect"]}</code>/' \
           f'<code>{user_data["next_respect"]}</code>\n' \
           f'<b>Деньги</b> – $<code>{user_data["money"]}</code>\n\n' \
           f'<b>Номер телефона</b> – (в разработке)\n' \
           f'<b>Деньги в банке</b> – (в разработке)\n' \
           f'<b>Работа</b> – (в разработке)\n\n' \
           f'<b>Законопослушность</b> – (в разработке)\n' \
           f'<b>Номер дома</b> – (в разработке)'
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton('Назад', callback_data='mm'))
    return text, kb


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('mm'))
async def cb_menu(callback_query: types.CallbackQuery, user_data: dict, call_args: dict):

    # Статистика
    if call_args.get('m') == 'st':
        text, kb = await get_menu_statistics_text(user_data)
        await callback_query.message.edit_text(text, reply_markup=kb)
        await callback_query.answer()
        return

    text, kb = await get_menu_text(user_data)
    await callback_query.message.edit_text(text, reply_markup=kb)
    await callback_query.answer()
