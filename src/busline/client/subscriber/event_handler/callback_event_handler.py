import inspect
from dataclasses import dataclass, field
from typing import Callable, Any, Awaitable

from busline.event.event import Event
from busline.client.subscriber.event_handler.event_handler import EventHandler


@dataclass
class CallbackEventHandler(EventHandler):
    """
    Event handler that uses a pre-defined callback.
    Refactored to be compatible with multiprocessing (picklable).

    Author: Nicola Ricciardi
    """

    on_event_callback: Callable[[str, Event], Any]
    
    # Internal flag to store whether the callback is async or sync
    _is_coroutine: bool = field(init=False)

    def __post_init__(self):
        # Determine if the callback is a coroutine function once during init.
        # This avoids using inspect inside the hot path (handle method).
        self._is_coroutine = inspect.iscoroutinefunction(self.on_event_callback)

    async def handle(self, topic: str, event: Event):
        if self._is_coroutine:
            await self.on_event_callback(topic, event)
        else:
            # Execute the synchronous callback directly.
            # In a multiprocessing context, this runs inside the worker process,
            # so it does not block the main event loop.
            self.on_event_callback(topic, event)