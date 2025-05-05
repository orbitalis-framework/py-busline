from typing import Callable
from dataclasses import dataclass
from busline.event.event import Event
from busline.client.subscriber.event_handler.event_handler import EventHandler


@dataclass
class ClosureEventHandler(EventHandler):
    """
    Event handler which use a pre-defined callback as `on_event`

    Author: Nicola Ricciardi
    """

    on_event_callback: Callable[[str, Event], None]

    async def handle(self, topic: str, event: Event):
        self.on_event_callback(topic, event)
