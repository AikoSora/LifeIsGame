from aiogram.types import (
    InlineKeyboardMarkup as IKM,
    InlineKeyboardButton as IKB,
    ReplyKeyboardMarkup as RKM,
    KeyboardButton as KB,
    Message,
    CallbackQuery,
)

from app.bot.router import Router
from app.models import User
from app.crud import get_tasks, create_user_task, get_user_task
from app.services import pagination, get_difficulty
from app.text import Tasks as TaskMessage

from typing import TYPE_CHECKING, Literal

from asyncio import create_task

from datetime import datetime

if TYPE_CHECKING:
    from aiogram import Bot
    from app.models import Tasks


router = Router(__name__)


def get_tasks_keyboard(completed: bool) -> list:
    return [
        [
            KB(text='Создать'),
            KB(text='Выполненные' if not completed else 'Задания'),
        ],
        [
            KB(text='Меню'),
        ],
    ]


async def __task_list(
    object: Literal['Message', 'CallbackQuery'],
    path_args: list[str],
    user: User,
    completed: bool = False
) -> None:
    ''' Function to send task list '''

    tasks = get_tasks(user=user, completed=completed)

    text = TaskMessage.TASK_LIST if not completed else TaskMessage.TASL_COMPLETED_LIST

    if not await tasks.acount():
        text += TaskMessage.TASK_LIST_NOT_FOUND if not completed else TaskMessage.TASK_COMPLETED_LIST_NOT_FOUND

        return await user.reply(
            text=text,
            reply_markup=RKM(keyboard=get_tasks_keyboard(completed=completed), resize_keyboard=True)
        )

    start, end = path_args[1].split(':') if len(path_args) > 1 else (None, None)

    page, pagination_start, pagination_end, page_count = pagination(
        objects_count=await tasks.acount(),
        start=int(start) if start else start,
        end=int(end) if end else end,
    )

    keyboard = []

    async for task in tasks.order_by('-pk')[pagination_start:pagination_end]:
        keyboard.append([
            IKB(
                text=f'{task.handled_title} ({task.handled_diff}) {"⏳" if task.started_at and not completed else ""}',
                callback_data=f'task {task.id}' + (' completed' if completed else '')
            )
        ])

    keyboard = list(reversed(keyboard))

    keyboard.append([
        IKB(
            text='◀️',
            callback_data=f'task_list{"_completed" if completed else ""} {pagination_end}:{pagination_end+5}' if page > 1 else 'pass'
        ),
        IKB(
            text=f'{page}/{page_count} ({await tasks.acount()})',
            callback_data="pass",
        ),
        IKB(
            text='▶️',
            callback_data=f'task_list{"_completed" if completed else ""} {pagination_start-5}:{pagination_start}' if page < page_count else 'pass',
        ),
    ])

    if isinstance(object, Message):
        await user.reply(text=text, reply_markup=IKM(inline_keyboard=keyboard))

        await user.reply(
            text=TaskMessage.TASK_CHOICE if not completed else TaskMessage.TASK_COMPLETED_CHOICE,
            reply_markup=RKM(keyboard=get_tasks_keyboard(completed=completed), resize_keyboard=True)
        )

    elif isinstance(object, CallbackQuery):
        await object.message.edit_text(
            text=text,
            reply_markup=IKM(inline_keyboard=keyboard)
        )


@router.message(names='задания', dialog=User.Dialog.DEFAULT)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    user.dialog = User.Dialog.TASKS
    await user.asave()

    create_task(
        __task_list(
            object=message,
            path_args=path_args,
            user=user,
        )
    )


@router.message(names='задания', dialog=User.Dialog.TASKS)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    user.dialog = User.Dialog.TASKS
    await user.asave()

    create_task(
        __task_list(
            object=message,
            path_args=path_args,
            user=user,
        )
    )


@router.message(names='выполненные', dialog=User.Dialog.TASKS)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    create_task(
        __task_list(
            object=message,
            path_args=path_args,
            user=user,
            completed=True,
        )
    )


@router.message(names='создать', dialog=User.Dialog.TASKS)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    user.dialog = User.Dialog.TASK_TITLE
    await user.asave()

    await user.reply(
        text=TaskMessage.TASK_INPUT_TITLE,
    )


@router.message(names='', dialog=User.Dialog.TASK_TITLE)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    user.temp_title = message.text
    user.dialog = User.Dialog.TASK_DESCRIPTION

    await user.asave()

    await user.reply(
        text=TaskMessage.TASK_INPUT_DESCRIPTION,
    )


@router.message(names='', dialog=User.Dialog.TASK_DESCRIPTION)
async def _(
    message: 'Message',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    await create_user_task(
        user=user,
        title=user.temp_title,
        description=message.text,
        difficulty=await get_difficulty(message.text),
    )

    user.dialog = User.Dialog.TASKS
    await user.asave()

    create_task(
        __task_list(
            object=message,
            path_args=[],
            user=user,
        )
    )


@router.callback(name='task_list')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    create_task(
        __task_list(
            object=event,
            path_args=path_args,
            user=user,
        )
    )


@router.callback(name='task_list_completed')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    create_task(
        __task_list(
            object=event,
            path_args=path_args,
            user=user,
            completed=True,
        )
    )


@router.callback(name='task')
async def _(
    event: 'CallbackQuery',
    path_args: list[str],
    user: User,
    bot: 'Bot',
) -> None:
    if len(path_args) < 2 or not path_args[1].isdigit():
        return

    task: 'Tasks' = await get_user_task(user=user, task_id=path_args[1])

    if path_args[-1] == 'delete':
        task.is_active = False
        await task.asave()

        return await event.message.edit_text(
            text=TaskMessage.TASK_ACTION_DELETE,
            reply_markup=IKM(inline_keyboard=[
                [IKB(
                    text='Назад',
                    callback_data=f'task_list{"_completed" if "completed" in path_args else ""}'
                )]
            ])
        )

    text = f"{task.title.title()} ({task.handled_diff}):\n\n"
    text += f"{task.get_description()}"

    if path_args[-1] == "start":
        task.started_at = datetime.now()

    elif path_args[-1] == "end":
        task.completed_at = datetime.now()

    await task.asave()

    keyboard = []
    keyboard_group = []

    if not task.completed_at:
        if task.started_at:
            keyboard_group.append(
                IKB(text='Завершить', callback_data=f'task {task.id} end')
            )
        else:
            keyboard_group.append(
                IKB(text='Начать', callback_data=f'task {task.id} start')
            )

    keyboard_group.append(
        IKB(
            text='Удалить',
            callback_data=f'task {task.id}{" completed" if "completed" in path_args else ""} delete'
        ),
    )

    keyboard.append(keyboard_group)
    keyboard.append(
        [IKB(
            text='Назад',
            callback_data=f'task_list{"_completed" if "completed" in path_args else ""}'
        )]
    )

    await event.message.edit_text(
        text=text,
        reply_markup=IKM(inline_keyboard=keyboard)
    )
