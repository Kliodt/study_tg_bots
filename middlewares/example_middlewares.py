from datetime import datetime
from random import randint
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


# Допустим мидлварь, которая достает user id из какого то стороннего сервиса
class GetUserIdMiddleware(BaseMiddleware):
    # эмуляция получения id
    def get_id(self, user_id: int):
        return randint(100_000_000, 900_000_000) + user_id

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user = data["event_from_user"] # так user передается в data
        data["my_user_id"] = self.get_id(user.id)
        return await handler(event, data)

# Мидлварь, которая вычисляет "счастливый месяц" пользователя
class HappyMonthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # получаем значение из предыдущей мидлвари
        my_user_id: int = data["my_user_id"]
        current_month = datetime.now().month
        is_happy_month: bool = (my_user_id % 12) == current_month
        # Кладём True или False в data, чтобы забрать в хэндлере
        data["is_happy_month"] = is_happy_month
        return await handler(event, data)

