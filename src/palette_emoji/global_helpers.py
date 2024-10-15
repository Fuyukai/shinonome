
from typing import Any

import outcome

from palette_emoji.internals.task import Task
from palette_emoji.run import DARK_HISTORY


def get_current_task() -> Task:
    """
    gets da current task (i.e. you)
    """

    ctx = DARK_HISTORY.get()
    return ctx.current_task


def reschedule(task: Task) -> None:
    """
    reschedules da task
    """

    ctx = DARK_HISTORY.get()
    ctx.reschedule(task)


async def wait_until_rescheduled(yield_value: Any) -> outcome.Outcome[Any]:
    """
    waits until da reschedule

    this is a low level function! do not use unless u know what youre doing!
    """

    task = get_current_task()
    return await task.suspend(yield_value)
