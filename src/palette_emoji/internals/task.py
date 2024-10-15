
import types
from collections.abc import Coroutine, Generator
from typing import Any

import attr
import outcome


class _RESULT_UNSET:
    pass

RESULT_UNSET = _RESULT_UNSET()

@types.coroutine
def _do_generator_suspend() -> Generator[None, outcome.Outcome[Any], Any]:
    return (yield)


@attr.define(slots=True, kw_only=True)
class Task:
    gen: Coroutine[None, outcome.Outcome[Any] | None, Any] = attr.field()
    result: Any | _RESULT_UNSET = attr.field(default=RESULT_UNSET, init=False)
    next_send: outcome.Outcome[Any] | None = attr.field(default=None, init=False)

    @property
    def running(self) -> bool:
        return self.result == RESULT_UNSET
    
    async def suspend(self) -> outcome.Outcome[Any]:
        """
        low level cancellation function, do not call (✼ X̥̥̥ ‸ X̥̥̥)
        """

        return (await _do_generator_suspend())

    def step(self) -> Any:
        """
        runs
        """

        try:
            return self.gen.send(self.next_send)
        except StopIteration as e:
            self.result = e.value
            return None
