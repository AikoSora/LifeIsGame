from app.services import get_fernet_client

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import User
    from datetime import datetime


class TaskMixin(object):
    user: 'User'
    title: str
    description: bytes
    difficulty: str
    is_active: bool
    started_at: 'datetime'
    completed_at: 'datetime'

    @property
    def handled_title(self) -> str:
        return self.title.title()[:20] + ('...' if len(self.title) > 20 else '')

    @property
    def handled_diff(self) -> str:
        return self.difficulty.upper()

    def get_description(self) -> str:
        ''' Decrypting task description and return this '''

        return get_fernet_client().decrypt(
            self.description
        ).decode()

    def set_description(self, text: str) -> None:
        ''' Encrypt task description and save this '''

        self.description = get_fernet_client().encrypt(
            data=text.encode(),
        )

    def __str__(self) -> str:
        return f'{self.handled_title} ({self.handled_diff})'

    __repr__ = __str__
