from aiogram import Dispatcher

from .is_admin import AdminFilter
from .is_group import IsGroupFilter
from .is_private import IsPrivateFilter
from .in_progress import InProgressFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroupFilter)
    dp.filters_factory.bind(IsPrivateFilter)
    dp.filters_factory.bind(InProgressFilter)
