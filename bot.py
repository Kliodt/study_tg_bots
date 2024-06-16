import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold

from config_private import TOKEN

# Крутой и довольно полный гайд: https://mastergroosha.github.io/aiogram-3-guide/

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

# Присвоить диспетчеру иммутабельные параметры, которые будут нужны в хэндлерах
dp["start_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
dp["dots_list"] = []


@dp.message(Command("start"))
async def command_start(message: Message) -> None:
    content = Text("Hello, ", Bold(message.from_user.full_name))
    # Короч тут далее метод as_kwargs возвращает словарь {text: ..., entities: ..., parse_mode: ...}
    # ** - используется для передачи словаря как именованных аргументов функции.
    # а надо это все для того, чтобы в сообщении был жирный текст и разметка не сломалась если message.from_user.full_name содержит < или >
    # (если текст заранее целиком известен, то его можно просто передать как HTML - см. command_info)
    await message.answer(**content.as_kwargs())

@dp.message(Command("echo"))
async def command_echo(message: Message, command: CommandObject) -> None:
    if command.args is None:
        await message.answer("нет аргумента")
    else:
        await message.answer(command.args)

@dp.message(Command("info"))
async def command_info(message: Message, started_at: str) -> None:
    await message.answer(f"Бот запущен <b>{started_at}</b>")

@dp.message(Command("list"))
async def command_list(message: Message, dots_list: list) -> None:
    dots_list.append(12)
    await message.answer(f"Лист: {dots_list}")





async def main() -> None:
    default_bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # тут ещё много других интересных настроек
    )
    bot = Bot(token=TOKEN, default=default_bot_properties)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())