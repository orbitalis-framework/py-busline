from typing import Callable, Coroutine, Dict, override, List
from dataclasses import dataclass

from busline.client.subscriber.topic_subscriber.event_handler.schemafull_handler import SchemafullEventHandler
from busline.event.event import Event
from busline.client.subscriber.topic_subscriber.event_handler.event_handler import EventHandler


@dataclass
class CallbackEventHandler(EventHandler):
    """
    Event handler which use a pre-defined callback

    Author: Nicola Ricciardi
    """

    on_event_callback: Callable[[str, Event], Coroutine]

    async def handle(self, topic: str, event: Event):
        await self.on_event_callback(topic, event)


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

