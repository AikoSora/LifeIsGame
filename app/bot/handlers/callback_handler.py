from aiogram.types import CallbackQuery
from .base import BaseEventHandler


class CallBackHandler(BaseEventHandler):
    """
    ----------------------
    CallBack Handler class
    ----------------------
    """

    async def __call__(self, object: CallbackQuery):

        self.message_from = object.from_user
        _, self.path_args = self.text_processing(object.data)

        self.user = await self.get_or_create_user(
            user_id=self.message_from.id,
            first_name=self.message_from.first_name,
            last_name=self.message_from.last_name,
            username=self.message_from.username
        )

        self.user.as_(self.bot)
        self.user.peer_id = self.user.tg_id

        for command in self.commands:
            command.register_data(
                object=object,
                path_args=self.path_args,
                user=self.user,
                bot=self.bot
            )

            if command.allowed_name():
                if not await command.execute():
                    await object.bot.answer_callback_query(
                        callback_query_id=object.id,
                        text='❌ Возникла ошибка при обработке события',
                        show_alert=True
                    )
                break
        else:
            await object.answer_callback_query(
                callback_query_id=object.id,
                text='❌ Неизвестный запрос',
                show_alert=True
            )
