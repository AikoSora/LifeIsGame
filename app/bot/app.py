from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TEST, PRODUCTION

from .filters import ChatTypeFilter
from .routes import routes
from .handlers import (
    MessageHandler,
    CallBackHandler,
)

from typing import TYPE_CHECKING
from os import environ
from asyncio import get_event_loop

import logging

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop


class Application:
    messages = []
    callbacks = []
    supergroups = []
    inlinequerys = []

    def __init__(
        self,
        *args,
        token: str,
        debug: bool = False,
        test_mode: bool = False,
        loop: 'AbstractEventLoop' = None,
        **kwargs,
    ) -> None:

        environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

        self.loop = loop or get_event_loop()
        self.logger = logging.getLogger(__name__)

        self.__debug = debug
        self.__test_mode = test_mode
        self.__token = token

        if self.__debug is True:
            logging.basicConfig(level=logging.DEBUG)

        self.load_commands()

        self.__initialize()

    def get_aiogram_bot_object(self) -> Bot:
        session = AiohttpSession(api=TEST if self.__test_mode else PRODUCTION)

        return Bot(
            token=self.__token,
            session=session,
        )

    def __initialize(self):
        """Function to initialize bot"""

        self.__bot = self.get_aiogram_bot_object()
        self.__dp = Dispatcher()

        me = self.loop.run_until_complete(
            self.__bot.get_me()
        )

        self.__dp.message.register(
            MessageHandler(self.messages, self.__bot, me.username).__call__,
            ChatTypeFilter("private"),
        )

        self.__dp.callback_query.register(
            CallBackHandler(self.callbacks, self.__bot, me.username).__call__,
        )

    async def _run(self):
        """
        Deleting not handled updates and run bot
        """

        await self.__bot.delete_webhook(drop_pending_updates=True)
        await self.__dp.start_polling(self.__bot, handle_signals=False)

    def start_polling(self):
        """
        Start main polling
        """

        self.loop.run_until_complete(
            self._run()
        )

    def load_commands(self):
        for route in routes:

            for command in route.messages:
                self.messages.append(command)

            for command in route.callbacks:
                self.callbacks.append(command)

            self.logger.info(f'{route.name} is loaded')
