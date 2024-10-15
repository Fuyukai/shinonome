from __future__ import annotations

import contextvars
from collections import deque
from collections.abc import Callable, Coroutine
from typing import Any, cast

import attr

from palette_emoji.internals.task import Task

DARK_HISTORY: contextvars.ContextVar[Runner] = contextvars.ContextVar("fesdfdsadf")


@attr.define(slots=True, kw_only=True)
class Runner:
    run_next_step: deque[Task] = attr.field(factory=deque)
    # weird, quasi-half-initiated field
    current_task: Task = attr.field(init=False)

    def reschedule(self, task: Task):
        self.run_next_step.append(task)

    def run_until_complete[T](self, initial_fn: Callable[[], Coroutine[Any, Any, T]]) -> T:
        task = Task(gen=initial_fn())
        self.run_next_step.appendleft(task)

        while task.running:
            try:
                recent = self.run_next_step.popleft()
            except IndexError:
                raise RuntimeError(
                    "no tasks to run ૮(˶╥︿╥)ა stop calling wait_until_rescheduled!!!!"
                ) from None

            self.current_task = recent

            if (yielded := recent.step()):
                raise ValueError(f"unexpected yield ╥﹏╥ don't send me a {yielded} please!")

        return cast(T, task.result)


def run_async_function[T](fn: Callable[[], Coroutine[Any, Any, T]]) -> T:
    runner = Runner()
    token: contextvars.Token[Runner] = DARK_HISTORY.set(runner)
    try:
        return runner.run_until_complete(fn)
    finally:
        DARK_HISTORY.reset(token)
