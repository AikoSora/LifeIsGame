from aiogram.types import (
    InlineKeyboardMarkup as IKM,
    InlineKeyboardButton as IKB,
)

from app.bot.router import Router
from app.models import User
from app.text import Start

from typing import TYPE_CHECKING

from asyncio import create_task

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message, CallbackQuery


router = Router(__name__)


async def __start(user: User):
    await user.reply(
        text=Start.START_MESSAGE,
        reply_markup=IKM(
            inline_keyboard=[
                [IKB(text='Да!', callback_data='continue')],
            ]
        )
    )


async def __edit_text(
    event: 'CallbackQuery',
    text: str | list,
    payload: str,
    keyboard_text: str = 'Далее',
):
    processed_text = '\n'.join(text) if isinstance(text, list) else text

    await event.message.edit_text(
        text=processed_text,
        reply_markup=IKM(inline_keyboard=[
            [
                IKB(
                    text=keyboard_text,
                    callback_data=payload
                )
            ]
        ])
    )


@router.message(names='/start', dialog=User.Dialog.START)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __start(user)
    )


@router.callback(name='continue')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_ZERO,
            payload='continue_one',
        )
    )


@router.callback(name='continue_one')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_ONE,
            payload='continue_two',
        )
    )


@router.callback(name='continue_two')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_TWO,
            payload='continue_three',
        )
    )


@router.callback(name='continue_three')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_THREE,
            payload='continue_four',
        )
    )


@router.callback(name='continue_four')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_FOUR,
            payload='continue_five',
        )
    )


@router.callback(name='continue_five')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    create_task(
        __edit_text(
            event=event,
            text=Start.CONTINUE_STAGE_FIVE,
            payload='continue_end',
            keyboard_text='Готов',
        )
    )


@router.callback(name='continue_end')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    user.dialog = User.Dialog.DEFAULT

    await event.message.delete()

    await user.asave()
    await user.return_menu()
