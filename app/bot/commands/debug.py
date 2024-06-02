from app.bot.router import Router
from app.models import User

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message


router = Router(__name__)


@router.message(names='/reset')
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot'
) -> None:
    ''' DEBUG COMMAND (RESET ALL USER DATA) '''

    from django.conf import settings

    if not settings.DEBUG:
        return

    user.dialog = User.Dialog.START

    await user.asave()
    await user.tasks.all().adelete()
    await user.reply('Done')
