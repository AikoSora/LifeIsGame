from .models import Tasks

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import User

    from django.db.models import BaseManager


def get_tasks(user: 'User', completed: bool) -> 'BaseManager':
    ''' Get all user tasks '''

    tasks = Tasks.objects.filter(user=user, is_active=True)

    if completed:
        return tasks.exclude(completed_at=None)
    return tasks.filter(completed_at=None)


async def create_user_task(
    user: 'User',
    title: str,
    description: str,
    difficulty: str,
) -> None:
    ''' Create user task '''
    task = Tasks()
    task.user = user
    task.title = title
    task.set_description(description)
    task.difficulty = difficulty

    await task.asave()


async def get_user_task(
    user: 'User',
    task_id: str | int,
    task: 'Tasks' = None,
) -> 'Tasks':
    ''' Get user task '''

    if task:
        return task

    return await Tasks.objects.filter(user=user, id=task_id).afirst()
