from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class ChatTypeFilter(BaseFilter): # Обязательно наследоваться от базового класса
    def __init__(self, chat_type: Union[str, list]): # У фильтра будет 1 аргумент, который может быть строкой или списком
        self.chat_type = chat_type

    # Справка по Python: метод __call__ позволяет вызвать экземпляр как функцию: my_obj=MyClass(); my_obj()
    async def __call__(self, message: Message) -> bool:  # метод с проверкой
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


        