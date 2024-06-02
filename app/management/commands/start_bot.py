from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import autoreload

from app.bot.app import Application


class Command(BaseCommand):
    help = 'Start Telegram bot'

    def handle(self, *args, **options):
        app = Application(
            token=settings.API_TOKEN,
            debug=settings.DEBUG,
            test_mode=settings.TEST_MODE,
        )

        if settings.DEBUG:
            autoreload.run_with_reloader(
                app.start_polling
            )
        else:
            app.start_polling()
