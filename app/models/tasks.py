from django.db import models
from .base import User
from app.bot.middlewares.tasks.mixin import TaskMixin


class Tasks(models.Model, TaskMixin):

    class Difficulty(models.TextChoices):
        EASY = 'easy'
        NORMAL = 'normal'
        HARD = 'hard'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    # User object

    # Title task
    title = models.TextField(null=False)

    # Description task
    description = models.BinaryField(null=False)

    # Difficulty task
    difficulty = models.CharField(
        choices=Difficulty.choices,
        max_length=9,
        null=True,
        default=None,
        blank=True
    )

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(default=None, null=True)

    is_active = models.BooleanField(default=True)
