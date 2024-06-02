from .base_command_handler import BaseCommandHandler


class MessageCommandHandler(BaseCommandHandler):
    """
    -----------------------
    Message Command Handler
    -----------------------
    """


class CallBackCommandHandler(BaseCommandHandler):
    """
    ------------------------
    CallBack Command Handler
    ------------------------
    """

    def register_data(self, object, path_args, user, bot):
        self.object = object
        self.path_args = path_args
        self.user = user
        self.bot = bot

    def allowed_name(self) -> bool:
        return self.command_name == self.path_args[0]
