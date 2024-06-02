from .models import Tasks

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User


async def get_tasks(user: 'User'):
    """ Get all user tasks """

    ...
