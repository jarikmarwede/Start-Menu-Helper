"""A thread that is stoppable."""
import threading
from typing import Any


class StoppableThread(threading.Thread):
    """Thread class with a stop() method.

    The thread itself has to check regularly for the stopped() condition.

    Copied from: https://stackoverflow.com/a/325528
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._stop_event: threading.Event = threading.Event()

    def stop(self) -> None:
        """Signals to the thread that it should stop."""
        self._stop_event.set()

    def stopped(self) -> bool:
        """Return whether the thread is supposed to be stopped."""
        return self._stop_event.is_set()
