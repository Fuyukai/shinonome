
from collections.abc import Coroutine
from typing import Any

import attr


class _RESULT_UNSET:
    pass

RESULT_UNSET = _RESULT_UNSET()


@attr.define(slots=True, kw_only=True)
class Task:
    gen: Coroutine[Any, Any, Any] = attr.field()
    result: Any | _RESULT_UNSET = attr.field(default=RESULT_UNSET)

    @property
    def running(self) -> bool:
        return self.result == RESULT_UNSET

    def step(self) -> Any:
        """
        runs
        """

        try:
            self.gen.send(None)
        except StopIteration as e:
            self.result = e.value
