from aiogram import Bot
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.enums import ParseMode
from aiogram.types import (
    ReplyKeyboardMarkup as RKM,
    KeyboardButton as KB,
    Message,
)

from copy import deepcopy

from typing import TYPE_CHECKING, Awaitable, TypeAlias

import logging
import asyncio

if TYPE_CHECKING:
    from typing import Callable


_Message: TypeAlias = Awaitable[Message | None] | Message | None
_logger = logging.getLogger(__name__)


class BaseMixin(object):
    __peer_id: int

    __bot: Bot

    @property
    def peer_id(self):
        return self.__peer_id

    @peer_id.setter
    def peer_id(self, value):
        self.__peer_id = value

    def return_menu(self, text: str | None = None, **kwargs) -> _Message:
        if not text:
            text = 'Добро пожаловать в Life!'

        keyboard = RKM(keyboard=[
            [KB(text='Задания'), KB(text='Рейтинг')],
            [KB(text='Статистика')],
        ], resize_keyboard=True)

        return self.reply(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
            **kwargs
        )

    def reply(self, text: str | list, reply_markup=None, **kwargs) -> _Message:
        processed_text = '\n'.join(text) if isinstance(text, list) else text

        context = {
            'chat_id': self.peer_id,
            'reply_markup': reply_markup,
            'parse_mode': ParseMode.HTML,
        }

        extra_context = deepcopy(kwargs)

        if 'photo' in extra_context:
            del extra_context['photo']

        if 'media' in extra_context:
            del extra_context['media']

        if 'animation' in extra_context:
            del extra_context['animation']

        context |= extra_context

        if 'photo' in kwargs and kwargs['photo'] is not None:
            context |= {
                'caption': processed_text,
                'photo': kwargs['photo'],
            }

            if 'disable_web_page_preview' in context:
                del context['disable_web_page_preview']

            callable_method = self.__bot.send_photo

        elif 'media' in kwargs and kwargs['media'] is not None:
            kwargs['media'][0].parse_mode = ParseMode.HTML
            kwargs['media'][0].caption = processed_text

            context |= {
                'media': kwargs['media'],
            }

            if 'disable_web_page_preview' in context:
                del context['disable_web_page_preview']

            if 'parse_mode' in context:
                del context['parse_mode']

            if 'reply_markup' in context:
                del context['reply_markup']

            callable_method = self.__bot.send_media_group

        elif 'animation' in kwargs and kwargs['animation'] is not None:
            context |= {
                'caption': processed_text,
                'animation': kwargs['animation'],
            }

            callable_method = self.__bot.send_animation

        else:
            context['text'] = processed_text

            callable_method = self.__bot.send_message

        try:
            event_loop = asyncio.get_running_loop()
        except RuntimeError:
            event_loop = None

        if event_loop is None:
            event_loop = asyncio.get_event_loop()

            message = event_loop.run_until_complete(
                event_loop.create_task(
                    self._call_bot_safe(callable_method, **context)
                )
            )

            return message
        else:
            return self._call_bot_safe(callable_method, **context)

    def as_(self, bot: Bot) -> None:
        self.__bot = bot

    @classmethod
    async def _call_bot_safe(cls, method: 'Callable', **kwargs) -> any:
        response = None

        try:
            response = await method(**kwargs)
        except TelegramUnauthorizedError:
            _logger.warning(
                f'Can\'t call aiogram method by specified params: {kwargs}',
                exc_info=True
            )
        except Exception as e:
            _logger.error(f'Unknown error: {str(e)}', exc_info=True)

        return response
