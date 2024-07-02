from typing import Optional

from aiogram import Router, F
from aiogram.enums import DiceEmoji
from aiogram.filters import Command
from aiogram.types import Message, PhotoSize, Chat

from filters.chat_type import ChatTypeFilter
from filters.find_usernames import HasUsernamesFilter

router = Router()

@router.message(Command(commands=["dice"]), ChatTypeFilter(chat_type=["group", "supergroup"]))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)

@router.message(F.text, HasUsernamesFilter())
async def message_with_usernames(message: Message, usernames: list[str]):
    await message.reply(
        f'Спасибо! Обязательно подпишусь на '
        f'{", ".join(usernames)}'
    )


@router.message(F.photo[-1].as_("largest_photo"))
async def forward_from_channel_handler(message: Message, largest_photo: PhotoSize) -> None:
    print(largest_photo.width, largest_photo.height)

