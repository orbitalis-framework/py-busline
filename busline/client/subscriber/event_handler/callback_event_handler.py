import inspect
from typing import Callable, Coroutine, Dict, override, List, Any, Awaitable
from dataclasses import dataclass, field

from busline.client.subscriber.event_handler.schemafull_handler import SchemafullEventHandler
from busline.event.event import Event
from busline.client.subscriber.event_handler.event_handler import EventHandler


@dataclass
class CallbackEventHandler(EventHandler):
    """
    Event handler which use a pre-defined callback

    Author: Nicola Ricciardi
    """

    on_event_callback: Callable[[str, Event], Any]

    __actual_async_on_event_callback: Callable[[str, Event], Awaitable] = field(init=False)

    def __post_init__(self):
        if not inspect.iscoroutinefunction(self.on_event_callback):

            async def async_wrapper(topic: str, event: Event) -> Callable[[str, Event], Awaitable]:
                return self.on_event_callback(topic, event)

            self.__actual_async_on_event_callback = async_wrapper

        else:
            self.__actual_async_on_event_callback = self.on_event_callback

    async def handle(self, topic: str, event: Event):
        await self.__actual_async_on_event_callback(topic, event)


@dataclass
class SchemafullCallbackEventHandler(SchemafullEventHandler):
    """
    Event handler which use a pre-defined callback

    Author: Nicola Ricciardi
    """

    schemas: List[Dict]
    on_event_callback: Callable[[str, Event], Coroutine]

    @override
    def input_schemas(self) -> List[Dict]:
        return self.schemas

    async def handle(self, topic: str, event: Event):
        await self.on_event_callback(topic, event)

