import logging
from dataclasses import dataclass, field
from typing import Optional, override, Callable, Awaitable

from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.client.subscriber.subscriber import Subscriber
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus
from busline.exceptions import EventBusClientNotConnected


@dataclass(eq=False)
class LocalSubscriber(Subscriber):
    """
    Subscriber topic-based which works with local eventbus

    Author: Nicola Ricciardi
    """

    eventbus: EventBus
    connected: bool = field(default=False)

    @override
    async def connect(self):
        logging.info(f"{self}: connecting...")
        self.connected = True

    @override
    async def disconnect(self):
        logging.info(f"{self}: disconnecting...")
        self.connected = False

    @override
    async def _internal_subscribe(self, topic: str, handler: Optional[EventHandler | Callable[[str, Event], Awaitable]] = None, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.add_subscriber(topic, self)

    @override
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.remove_subscriber(self, topic)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)