import asyncio
import datetime
import functools
from rich import print
from aiogram import types
""" Основные функции бота """


def run_sync(func, *args, **kwargs):
    """Run a non-async function in a new thread and return an awaitable"""
    # Returning a coro
    return asyncio.get_event_loop().run_in_executor(
        None,
        functools.partial(func, *args, **kwargs),
    )


def run_async(loop, coro):
    """Run an async function as a non-async function, blocking till it's done"""
    # When we bump minimum support to 3.7, use run()
    return asyncio.run_coroutine_threadsafe(coro, loop).result()


def send_logs(message: types.Message, error=None) -> None:
    """ Распечатывает логи в терминал """
    if error: error = "red"
    else: error = "white"
    print(f'[green bold]{datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}[/green bold] | [yellow bold]'
          f'{message.chat.id} ({message.chat.title or "PM"}) – ({message.from_user.id}) [/yellow bold]'
          f'[{error} bold]{message.from_user.full_name}[/{error} bold][yellow bold] → [{error} bold]'
          f'{message.text or message.content_type} [/{error} bold]({message.message_id})')
