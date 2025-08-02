import logging
from typing import override

from busline.client.publisher.publisher import Publisher
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus
from busline.exceptions import EventBusClientNotConnected
from dataclasses import dataclass, field


@dataclass(eq=False)
class LocalPublisher(Publisher):
    """
    Publisher which works with local eventbus, this class can be initialized and used stand-alone

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
    async def _internal_publish(self, topic: str, event: Event, **kwargs):

        if not self.connected:
            raise EventBusClientNotConnected()

        await self.eventbus.put_event(topic, event)

    def __eq__(self, other):
        return self.identifier == other.identifier

    def __hash__(self):
        return hash(self.identifier)