from aiogram import types
from aiogram.utils import exceptions
from loader import dp


@dp.errors_handler(exception=exceptions.MessageNotModified)
async def message_not_modified(update: types.Update, error: exceptions.MessageNotModified):
    return True


@dp.errors_handler(exception=exceptions.MessageToDeleteNotFound)
async def message_to_delete_not_found(update: types.Update, error: exceptions.MessageToDeleteNotFound):
    return True
