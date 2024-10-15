
import types
from collections.abc import Coroutine, Generator
from typing import Any

import attr
import outcome


class _RESULT_UNSET:
    pass

RESULT_UNSET = _RESULT_UNSET()

WAIT_UNTIL_RESCHEDULED = object()

@types.coroutine
def _do_generator_suspend(what: Any) -> Generator[Any, outcome.Outcome[Any], Any]:
    return (yield what)


@attr.define(slots=True, kw_only=True)
class Task:
    gen: Coroutine[Any, outcome.Outcome[Any] | None, Any] = attr.field()
    result: Any | _RESULT_UNSET = attr.field(default=RESULT_UNSET, init=False)
    next_send: outcome.Outcome[Any] | None = attr.field(default=None, init=False)

    @property
    def running(self) -> bool:
        return self.result == RESULT_UNSET
    
    async def suspend(self, what: Any) -> outcome.Outcome[Any]:
        """
        low level cancellation function, do not call (✼ X̥̥̥ ‸ X̥̥̥)
        """

        return (await _do_generator_suspend(what))

    def step(self) -> Any:
        """
        runs
        """

        try:
            return self.gen.send(self.next_send)
        except StopIteration as e:
            self.result = e.value
            return None
