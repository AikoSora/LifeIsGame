from aiogram.types import Message
from .base import BaseEventHandler


class MessageHandler(BaseEventHandler):
    """
    ---------------------
    Message handler class
    ---------------------
    """

    async def __call__(self, message: Message):

        self.message = message
        self.message_from = self.message.from_user
        self.command_name, self.path_args = self.text_processing(self.message.text)

        self.user = await self.get_or_create_user(
            user_id=self.message_from.id,
            first_name=self.message_from.first_name,
            last_name=self.message_from.last_name,
            username=self.message_from.username
        )

        self.user.as_(self.bot)
        self.user.peer_id = self.user.tg_id

        if not self.is_menu_command(self.command_name):
            for command in self.commands:
                command.register_data(
                    object=message,
                    name=self.command_name,
                    path_args=self.path_args,
                    user=self.user,
                    bot=self.bot
                )

                if command.allowed_name() and command.allowed_dialog():
                    if not await command.execute():
                        await self.message.reply(
                            "❌ Произошла <b>системная</b> ошибка. Выйдите в меню и попробуйте <b>ещё раз</b>.",
                            parse_mode='HTML'
                        )
                    break
            else:
                await self.message.reply(
                    "⚠️ Неизвестная команда. Напишите мне <b>«Меню»</b> и воспользуйтесь кнопками",
                    parse_mode='HTML'
                )
        else:
            await self.user.return_menu()
