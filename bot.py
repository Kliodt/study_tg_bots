import asyncio
from random import randint
from typing import Optional

from aiogram import html, F
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, LinkPreviewOptions, BufferedInputFile, FSInputFile, URLInputFile, KeyboardButton, \
    ReplyKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder

from config_private import TOKEN, ADMIN_CHAT_ID
from handlers import questions, different_types, happy_month

# Крутой и довольно полный гайд: https://mastergroosha.github.io/aiogram-3-guide/

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


# ---------------------------- Знакомство ---------------------------------------
# Присвоить диспетчеру иммутабельные параметры, которые будут нужны в хэндлерах
dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


# Создание и регистрация базовой команды
# @dp.message(Command("start"))
# async def command_start(message: Message) -> None:
#     await message.answer(f"Привет, {message.from_user.full_name}")


# Отправка сообщения по id чата, аргумент бот прокидывается в аргументах библиотекой,
# так же как и команда, из которой вытаскиваются ее аргументы
@dp.message(Command("send_to_admin"))
async def command_start(message: Message, command: CommandObject, bot: Bot) -> None:
    await bot.send_message(ADMIN_CHAT_ID, f"От пользователя: @{message.from_user.username}\nСообщение: {command.args}")


# Использование доп. параметров в функции.
# started_at - параметр устанавливается в начале этого файла: dp["started_at"] = ...
# info_req_count - используется global и изменяется внутри функции
info_request_count = 0
@dp.message(Command("info"))
async def command_info(message: Message, started_at: str) -> None:
    global info_request_count
    info_request_count += 1
    await message.answer(f"Бот запущен {started_at}\nКоличество запросов info: {info_request_count}")


# ---------------------------- Работа с сообщениями ---------------------------------------
# Если текст известен заранее можно делать прямо так
@dp.message(Command("formattings_1"))
async def command_start(message: Message) -> None:
    await message.answer("<b>Жирный</b> <i>Курсивный</i> <u>Подчеркнутый</u>")


# Если текст заранее не известен, то в нем могут случайно быть элементы HTML
@dp.message(Command("formattings_2"))
async def command_start(message: Message) -> None:
    content = Text("Hello, ", Bold(message.from_user.full_name))
    # Короч тут далее метод as_kwargs возвращает словарь {text: ..., entities: ..., parse_mode: ...}
    # ** - используется для передачи словаря как именованных аргументов функции.
    # а надо это все для того, чтобы в сообщении был жирный текст и разметка не сломалась если message.from_user.full_name содержит < или >
    await message.answer(**content.as_kwargs())


# html_text - для сохранения форматирования
@dp.message(Command("echo"))
async def command_echo(message: Message) -> None:
    await message.answer(message.html_text.replace("/echo", "", 1))


@dp.message(Command("links"))
async def command_links(message: Message) -> None:
    # пусть хотим отправить сообщение с 2 ссылками
    links_text = (
        "https://nplus1.ru/news/2024/05/23/voyager-1-science-data"
        "\n"
        "https://t.me/telegram"
    )
    # предпросмотр отключен
    my_options_1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(f"Нет превью:\n{links_text}", link_preview_options=my_options_1)

    # Маленькое превью
    # Для использования prefer_small_media обязательно указывать ещё и url
    my_options_2 = LinkPreviewOptions(prefer_small_media=True, url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data")
    await message.answer(f"Маленькое превью:\n{links_text}", link_preview_options=my_options_2)

    # Большое превью
    # Для использования prefer_large_media обязательно указывать ещё и url
    my_options_3 = LinkPreviewOptions(prefer_large_media=True, url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data")
    await message.answer(f"Большое превью:\n{links_text}", link_preview_options=my_options_3)


@dp.message(Command("get_images"))
async def command_get_images(message: Message) -> None:
    file_ids = []

    # 1. Прямая загрузка
    with open("my_img.png", "rb") as my_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
                my_buffer.read(),
                filename="any name i want"
            ),
            caption="Изображение из буфера"
        )
    file_ids.append(result.photo[-1].file_id)

    # 2. Из файловой системы
    image_from_pc = FSInputFile("my_img.png")
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)

    # 3. По ссылке
    image_from_url = URLInputFile("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQfLlqt_j1aK3Kd-e0xZXdGzyV3AT03VqSUU0pPuL39H2QlbZ1Gj6h6F9FfQQIyvhSj-DE&usqp=CAU")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)

    await message.answer("Отправленные файлы:\n" + "\n".join(file_ids))


@dp.message(Command("get_album"))
async def command_get_album(message: Message) -> None:
    album_builder = MediaGroupBuilder(
        caption="Текст общей подписи"
    )
    album_builder.add_photo(media=FSInputFile("my_img.png"))
    album_builder.add_photo(media=FSInputFile("my_img.png"))
    await message.answer_media_group(media=album_builder.build())


# ----------------------------- Кнопки -------------------------------------------
@dp.message(Command("choose"))
async def command_choose(message: Message) -> None:
    # kb - это матрица того, как будут располагаться кнопки (по рядам и столбцам)
    kb = [
        [KeyboardButton(text="A"), KeyboardButton(text="B")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Сделай выбор", reply_markup=keyboard)


@dp.message(Command("choose_number"))
async def command_choose_number(message: Message) -> None:
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(KeyboardButton(text=str(i)))
    builder.adjust(4,4,4,4)

    await message.answer("Сделай выбор числа", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(Command("url_buttons"))
async def command_url_buttons(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(InlineKeyboardButton(
        text="Оф. канал Telegram",
        url="tg://resolve?domain=telegram")
    )
    await message.answer("Выберите ссылку", reply_markup=builder.as_markup())


@dp.message(Command("callback_get_random"))
async def command_callback_get_random(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
            text="press me", callback_data="get_random"
    ))
    await message.answer("press the button below", reply_markup=builder.as_markup())

@dp.callback_query(F.data == "get_random")
async def callback_send_random_value(callback: CallbackQuery):
    await callback.message.answer(f"random number is: {str(randint(1, 10))}")
    await callback.answer("thanks")
    # или просто await callback.answer()

# Обязательно наследоваться от CallbackData и принимать значение prefix
class NumberCallbackFactory(CallbackData, prefix="number"):
    action: str
    value: Optional[int] = None

def build_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="+1", callback_data=NumberCallbackFactory(action="change", value=1)
    )
    builder.button(
        text="-1", callback_data=NumberCallbackFactory(action="change", value=-1)
    )
    builder.button(
        text="finish", callback_data=NumberCallbackFactory(action="finish")
    )
    builder.adjust(2) # выравниваем по 2 кнопки в ряд чтобы получилось 2+1
    keyboard = builder.as_markup()
    return keyboard

# обновляет текст сообщения с числом
async def update_num_text_fab(message: Message, new_value: int):
    await message.edit_text(
        f"Ваше число: {new_value}",
        reply_markup=build_keyboard()
    )

user_data = {}
@dp.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: Message):
    user_data[message.from_user.id] = 0
    await message.answer("Ваше число: 0", reply_markup=build_keyboard())


# обработка колбэков
@dp.callback_query(NumberCallbackFactory.filter())
async def process_callback(callback: CallbackQuery, callback_data: NumberCallbackFactory):
    # Имя параметра должно быть именно таким ----------> ^
    # текущее значение берем из нашего словаря
    user_value = user_data.get(callback.from_user.id, 0)
    if callback_data.action == "change":
        user_value += callback_data.value
        user_data[callback.from_user.id] = user_value
        await update_num_text_fab(callback.message, user_value)

    elif callback_data.action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()




async def main() -> None:
    default_bot_properties = DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # тут ещё много других интересных настроек
    )
    bot = Bot(token=TOKEN, default=default_bot_properties)

    dp.include_router(questions.router)
    dp.include_router(different_types.router)
    dp.include_router(happy_month.router)

    await bot.delete_webhook(drop_pending_updates=True) # пропустить все накопленные входящие сообщения
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())