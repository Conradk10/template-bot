from loader import dp
from aiogram import types


@dp.message_handler(commands=['register'])
async def cmd_register(message: types.Message, user_data: dict):
    text, kb = await get_register_text(user_data, state=0)
    await message.answer(text, reply_markup=kb)


async def get_register_text(user_data: dict, state: int) -> (str, types.InlineKeyboardMarkup):
    if state == 1:
        text = '<i>*Вы садитесь в самолет и улетаете из своего родного города*</i>'
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.insert(types.InlineKeyboardButton('Далее', callback_data='register a:next p:2'))
    elif state == 2:
        text = '<i>*Вы прилетели в город своей мечты и направляетесь оформлять ' \
               'документы в паспортный стол*</i>\n\n' \
               '<b>Вы</b>: - Здравствуйте, мне нужно оформить документы на получение паспорта.\n' \
               '<b>Сотрудник</b>: - Будьте добры, заполните вот эту анкету... <i>*Вам передали анкету*</i>'
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.insert(types.InlineKeyboardButton(
            'Заполнить анкету', web_app=types.WebAppInfo(url='https://vistate.x-net.pp.ua/register.html')
        ))
        # kb.insert(types.InlineKeyboardButton('Далее', callback_data='register a:next p:3'))
    elif state == 3:
        text = '<i>*Вы заполнили все бумаги и покинули паспортный стол*</i>'
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.insert(types.InlineKeyboardButton('Далее', callback_data='register a:next p:4'))
    elif state == 4:
        text = '<i>*По пути на вокзал Вас встретил какой-то незнакомец*</i>\n\n' \
               '<b>Незнакомец</b>: - Эй, привет! Новые люди в штате?\n' \
               '<b>Вы</b>: - Да, я только из паспортного стола.\n' \
               '<b>Незнакомец</b>: - Тебе очень повезло! ' \
               'В паспортном столе сказали что за паспортом еще зайти нужно?\n' \
               '<b>Вы</b>: - Эмм.. Нет.\n' \
               '<b>Незнакомец</b>; - Тогда я скажу: за паспортом нужно ' \
               'зайти в мэрию, без него никуда. Кстати, меня Томми зовут, будем знакомы.\n' \
               f'<b>Вы</b>: - Приятно познакомиться, Томми, меня зовут {user_data["surname"]}.\n' \
               '<b>Томми</b>: - Направляйся в мэрию за паспортом и ' \
               f'возвращайся ко мне, у меня еще будет для тебя работенка. ' \
               f'Удачи, {user_data["surname"]}.\n' \
               '<b>Вы</b>: - Ладно, бывай, Томми.\n\n' \
               '📌 <b>Квест</b>: направляйтесь в мэрию забрать паспорт.\n' \
               'ℹ️ <b>Совет</b>: используйте команду "Навигатор" для навигации по штату.'
        kb = types.InlineKeyboardMarkup(row_width=1)
        # kb.insert(types.InlineKeyboardButton('Далее', callback_data='register a:next p:5'))
    else:
        text = '<i>*Некоторым временем ранее*</i>\n\n' \
               '<b>?</b>: - Как же быстро летит время, ' \
               'только недавно мы вместе сидели за партой, ' \
               'но, вот ты уже собираешься в путь...\n' \
               '<b>Вы</b>: - Выбраться из этой дыры всегда ' \
               'было моей мечтой! Надеюсь в новом месте я ' \
               'добьюсь всех своих целей.\n' \
               '<b>?</b>: - У меня кое что для тебя есть.. ' \
               'Держи, это навигатор, тебе он точно пригодится! ' \
               '<i>*Вы взяли навигатор*</i>'
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.insert(types.InlineKeyboardButton('Далее', callback_data='register a:next p:1'))
    return text, kb


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('register'))
async def cb_menu(callback_query: types.CallbackQuery, user_data: dict, call_args: dict):

    # Статистика
    if call_args.get('a') == 'next':
        state = int(call_args.get('p'))
        text, kb = await get_register_text(user_data, state=state)
        await callback_query.message.delete_reply_markup()
        await callback_query.message.answer(text, reply_markup=kb)
        await callback_query.answer()
