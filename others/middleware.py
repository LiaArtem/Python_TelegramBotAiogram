import aiosqlite
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Dict, Any, Callable, Awaitable
from others.user_db_connect import User_DB_Request


# счетчик запусков /start
class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.counter += 1
        data['counter'] = self.counter
        return await handler(event, data)


# рабочий день с ПН-ПТ, с 8:00 по 19:00
def work_time() -> bool:
    return datetime.now().weekday() in (0, 1, 2, 3, 4) and datetime.now().hour in [i for i in (range(8, 19))]


# пишет пользователю сообщение если рабочее время истекло
class WorkTimeMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if work_time():
            return await handler(event, data)

        await event.answer(text='Бот працює з ПН-ПТ з 8:00 по 19:00')


# полная блокировка сообщений телеграмм если рабочее время истекло
class WorkTimeMiddlewareAllBlock(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if True:  # work_time():
            return await handler(event, data)


# логирование пользователей в таблицу
class UserDBSessionMiddleware(BaseMiddleware):
    def __init__(self, connection_string: str):
        super().__init__()
        self.connection_string = connection_string

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        async with aiosqlite.connect(self.connection_string) as db:
            data['request'] = User_DB_Request(db)
            return await handler(event, data)
