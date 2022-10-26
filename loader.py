from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data import config


bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML, validate_token=True)
# storage = RedisStorage2(**config.redis)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
