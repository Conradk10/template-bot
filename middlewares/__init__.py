from aiogram import Dispatcher

# from .throttling import ThrottlingMiddleware
from .big_brother import BigBrotherMiddleware
from .user_data import UserDataMiddleware
from .chat_data import ChatDataMiddleware


def setup(dp: Dispatcher):
    # dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(BigBrotherMiddleware())
    dp.middleware.setup(UserDataMiddleware())
    dp.middleware.setup(ChatDataMiddleware())
