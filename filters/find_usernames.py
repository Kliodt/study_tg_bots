from aiogram.filters import BaseFilter
from aiogram.types import Message


class HasUsernamesFilter(BaseFilter):
    def __call__(self, message: Message):
        entities = message.entities or []
        found_usernames = [el.extract_from(message.text) for el in entities if el.type == "mention"]
        if len(found_usernames) > 0:
            return {"usernames": found_usernames} # Если юзернеймы есть, то "проталкиваем" их в хэндлер
        return False # Иначе, вернём False


