from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from middlewares.example_middlewares import GetUserIdMiddleware, HappyMonthMiddleware
from middlewares.typing_middleware import TypingMiddleware

router = Router()

router.message.middleware(GetUserIdMiddleware())
router.message.middleware(HappyMonthMiddleware())
router.message.middleware(TypingMiddleware())

@router.message(Command("happymonth"), flags={"long_operation": "upload_video_note"})
async def command_happymonth(message: Message, my_user_id: int, is_happy_month: bool):
    phrases = [f"Ваш ID в нашем сервисе: {my_user_id}"]
    if is_happy_month:
        phrases.append("Сейчас ваш счастливый месяц!")
    else:
        phrases.append("В этом месяце будьте осторожнее...")
    await message.answer(". ".join(phrases))

