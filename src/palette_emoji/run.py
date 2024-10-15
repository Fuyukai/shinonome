
from collections import deque
from collections.abc import Callable, Coroutine
from typing import Any, cast

import attr

from palette_emoji.internals.task import Task


@attr.define(slots=True, kw_only=True)
class Runner:
    tasks: deque[Task] = attr.field(factory=deque)

    def run_until_complete[T](self, initial_fn: Callable[[], Coroutine[Any, Any, T]]) -> T:
        task = Task(gen=initial_fn())
        self.tasks.append(task)

        while task.running:
            recent = self.tasks.popleft()
            recent.step()

        return cast(T, task.result)


def run_async_function[T](fn: Callable[[], Coroutine[Any, Any, T]]) -> T:
    runner = Runner()
    return runner.run_until_complete(fn)
