from aiogram.types import (
    InlineKeyboardMarkup as IKM,
    InlineKeyboardButton as IKB,
)

from app.bot.router import Router
from app.models import User

from asyncio import sleep

from time import time


router = Router(__name__)


async def start(object, user, callback, language):
    if callback:
        text = "Привет!" if language == "ru" else "Hello!"
        language = "ru" if language == "en" else "en"

        await object.message.edit_text(f"{text} {time()}", reply_markup=IKM(inline_keyboard=[
            [IKB(text=f'{language.upper()}', callback_data=f'playboy {language}')],
        ]))
    else:
        await user.reply(f"Привет! {time()}", reply_markup=IKM(inline_keyboard=[
            [IKB(text='EN', callback_data="playboy en")],
        ]))


@router.message(names='/start', dialog=User.Dialog.START)
async def _(message, path_args, user, bot):
    await start(message, user, False, "")


@router.message(names='/info', dialog=User.Dialog.START)
async def test(message, path_args, user, bot):
    await sleep(10)
    await user.reply(f"info! {time()}")


@router.message(names='', dialog=User.Dialog.START)
async def _(message, path_args, user, bot):
    await sleep(10)
    await user.reply(f"Nothing! {time()}")


@router.callback(name="playboy")
async def _(event, path_args, user, bot):
    await start(event, user, True, path_args[-1])
