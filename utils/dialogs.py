from aiogram import types


def user_not_registred_dialog():
    text = 'Ты не зарегистрирован!'
    kb = types.InlineKeyboardMarkup()
    return text, kb
