from loader import dp
from aiogram import types


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('close'))
async def cb_close(callback_query: types.CallbackQuery):
    if callback_query.message.reply_to_message and \
            callback_query.from_user.id != callback_query.message.reply_to_message.from_user.id:
        await callback_query.answer(text='⛔️ Это действие не для тебя')
        return

    if callback_query.message.reply_to_message:
        try:
            await callback_query.message.reply_to_message.delete()
        except Exception:
            pass
    try:
        await callback_query.message.delete()
    except Exception:
        pass

    await callback_query.answer(text='✅ Закрыто')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('none'))
async def cb_close(callback_query: types.CallbackQuery):
    await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('none'))
async def cb_close(callback_query: types.CallbackQuery):
    await callback_query.answer()
