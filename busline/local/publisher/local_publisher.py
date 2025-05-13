import logging
from typing import override

from busline.client.publisher.publisher import Publisher
from busline.event.event import Event
from busline.local.eventbus.eventbus import EventBus
from busline.exceptions import EventBusClientNotConnected
from dataclasses import dataclass, field


@dataclass
class LocalEventBusPublisher(Publisher):
    """
    Publisher which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    eventbus: EventBus
    connected: bool = field(default=False)

    @override
    async def connect(self):
        logging.info(f"publisher {self.identifier} connecting...")
        self.connected = True

    @override
    async def disconnect(self):
        logging.info(f"publisher {self.identifier} disconnecting...")
        self.connected = False

    @override
    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):

        if not self.connected:
            raise EventBusClientNotConnected()

        await self.eventbus.put_event(topic_name, event)