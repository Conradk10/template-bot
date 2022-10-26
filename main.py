import asyncio
import aioschedule

from loader import dp
from aiohttp import web
from loguru import logger
from schedule import do_payday, do_checkout
from webapp.handlers import app
from aiogram.utils import executor
from utils.db.sqliter import connection


async def scheduler():
    """ Расписание """
    aioschedule.every().hour.at(':00').do(do_payday)    # Пейдей каждый час
    aioschedule.every().day.at('21:30').do(do_checkout)     # Каждый день банковский чек

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher: dp):
    """ Выполняется при запуске бота """
    from utils.misc import logging
    logging.setup()
    logger.info(f"Бот успешно загружен!")

    import middlewares
    middlewares.setup(dispatcher)

    import filters
    filters.setup(dispatcher)

    import handlers
    import keyboards

    asyncio.create_task(web._run_app(app, host="0.0.0.0", port=5001))
    asyncio.create_task(scheduler())


async def on_shutdown(dispatcher: dp):
    """ Выполняется при остановке бота """
    logger.info("Остановка...")

    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

    connection.close()

    logger.info("Бот успешно остановлен!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
