from django.db import models
from .mixins import TelegramMixin


class User(TelegramMixin):
    """ The main essence of the users LifeIsGame """

    class Dialog(models.TextChoices):
        START = 'start'
        DEFAULT = 'default'
        TASKS = 'tasks'
        TASK_TITLE = 'task_title'
        TASK_DESCRIPTION = 'task_description'

    dialog = models.TextField(default=Dialog.START)
    # Current user dialog

    is_active = models.BooleanField(
        verbose_name='активен',
        help_text='Если данное поле выключено, то данный пользователь считается забаненым',
        default=True,
    )
    # A field for deactivating an account instead of completely deleting it

    is_staff = models.BooleanField(verbose_name='сотрудник', default=False)
    # Determines whether the users can log in to the admin panel

    temp = models.TextField(default='', blank=True)
    temp_title = models.TextField(default='', blank=True)
    temp_description = models.TextField(default='', blank=True)
    # Temp variables

    created_at = models.DateTimeField(
        verbose_name='дата регистрации',
        auto_now_add=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name='дата обновления',
        auto_now=True,
        blank=True
    )
    # Timestamps
