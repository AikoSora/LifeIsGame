from ..base import BaseMixin


class TelegramUser(BaseMixin):
    tg_id: int
    tg_first_name: str | None
    tg_last_name: str | None
    tg_username: str | None

    dialog: str

    @property
    def username(self):
        return f'@{self.tg_username}' if self.tg_username else self.tg_first_name
