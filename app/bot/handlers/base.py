from app.models import User
from re import split as re_split
from typing import Tuple


class BaseEventHandler:

    """
    ------------------
    Base Event Handler
    ------------------

    @commands -> list[BaseCommandHandler]
    @bot -> Aiogram Bot
    """

    def __new__(cls, commands, bot, username):
        instance = super().__new__(cls)

        instance.commands = sorted(commands)
        instance.bot = bot
        instance.username = username

        return instance

    def text_processing(self, text: str | None) -> Tuple[str, list]:
        """
        ---------------------------
        Function for clearing text
        ---------------------------
        * text: string

        return: Tuple [ string, list ]
        """
        if text is None:
            return ('', '')

        processed_name = text.lower().strip()
        path_args = re_split(r'\s+', processed_name)

        return (processed_name, path_args)

    def is_menu_command(self, text) -> bool:
        """
        Function to check whether the message is a message about returning to the menu
        """
        return text == 'меню'

    async def get_or_create_user(
            self,
            user_id: int,
            first_name: str = None,
            last_name: str = None,
            username: str = None
    ):
        """
        ---------------------------
        Function for get user
        ---------------------------
        1) user_id: integer

        2) first_name:
            string (default: None)

        3) last_name:
            string (default: None)

        4) username:
            string (default: None)

        return: Account model
        """
        user = await User.objects.aget_or_create(
            tg_id=user_id,
            defaults={
                'tg_first_name': first_name,
                'tg_last_name': last_name,
                'tg_username': username
            }
        )

        return user[0]

    def __str__(self) -> str:
        return "(EHO) Event Handler Object"

    __repr__ = __str__
