from typing import Callable
from abc import ABC
from busline.event.event import Event
from busline.client.subscriber.listener.event_handler import EventHandler


class ClosureEventHandler(EventHandler, ABC):
    """
    Abstract event listener which use a pre-defined callback as `on_event`

    Author: Nicola Ricciardi
    """

    def __init__(self, on_event_callback: Callable[[str, Event], None]):
        EventHandler.__init__(self)

        self.__on_event_callback = on_event_callback

    async def on_event(self, topic: str, event: Event):
        self.__on_event_callback(topic, event)
