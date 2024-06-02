import logging
import sys
import traceback
from asyncio import create_task


class BaseCommandHandler:
    """
    ---------------
    Command handler
    ---------------

    @function -> Function
    @name -> str
    @dialog -> str (Default: None)
    @with_args -> bool (Default: True)
    """

    def __init__(
            self,
            function,
            name: str,
            dialog: str = None,
            with_args=True,
            *args,
            **kwargs
    ):
        self.command_name = name
        self.command_dialog = dialog
        self.command_with_args = with_args
        self.command_function = function

    def register_data(self, object, name, path_args, user, bot):
        """
        Function for register event data
        """

        self.object = object
        self.name = name
        self.path_args = path_args
        self.user = user
        self.bot = bot

    def allowed_name(self) -> bool:
        """
        Function for check command name to name

        @return -> bool
        """

        if self.command_with_args and len(self.path_args) > 0:
            return self.command_name in ['', self.path_args[0]]
        return self.command_name in ['', self.name]

    def allowed_dialog(self) -> bool:
        """
        Function for check command dialog to user dialog

        @return -> bool
        """
        if self.command_dialog is None:
            return True
        return self.command_dialog == self.user.dialog

    def get_function(self):
        return self.command_function(
            self.object,
            self.path_args,
            self.user,
            self.bot
        )

    async def execute(self):
        try:
            create_task(
                self.get_function()
            )
            return True
        except Exception:
            _, ex, tb = sys.exc_info()
            error_text = "\n"

            for text in traceback.format_tb(tb):
                error_text += text

            logging.error(error_text + f"{ex}")

            return False

    def __lt__(self, other):
        return len(self.command_name) > len(other.command_name)

    def __str__(self):
        return f"<EventHandler> command: {self.command_name}"

    __repr__ = __str__
