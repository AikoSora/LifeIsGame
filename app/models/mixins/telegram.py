from django.db import models

from app.bot.middlewares.user.mixin import TelegramUser


class TelegramMixin(models.Model, TelegramUser):
    """ Mixin for users authorization via Telegram """

    class Meta:
        abstract = True

    tg_id = models.PositiveBigIntegerField(
        verbose_name='Telegram ID',
        default=None,
        null=True,
        db_index=True
    )
    # Telegram users ID

    tg_username = models.TextField(
        verbose_name='Логин Telegram',
        default=None,
        null=True
    )
    # Telegram username (without @)

    tg_first_name = models.TextField(
        verbose_name='имя',
        default=None,
        null=True
    )
    # Telegram first name

    tg_last_name = models.TextField(
        verbose_name='фамилия',
        default=None,
        null=True
    )
    # Telegram last name


__all__ = (
    'TelegramMixin',
)
