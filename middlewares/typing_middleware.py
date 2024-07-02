from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender


class TypingMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        if long_operation_type:
            async with ChatActionSender(action=long_operation_type, chat_id=event.chat.id, bot=event.bot):
                return await handler(event, data)
        else:
            return await handler(event, data)

