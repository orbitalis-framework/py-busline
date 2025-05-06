import logging
from dataclasses import dataclass, field
from typing import Optional

from busline.client.subscriber.mhs import MultiHandlersSubscriber
from busline.local.eventbus.eventbus import EventBus
from busline.exceptions import EventBusClientNotConnected


@dataclass
class LocalEventBusMultiHandlersSubscriber(MultiHandlersSubscriber):
    """
    Abstract subscriber which works with local eventbus without implementing `on_event` method

    Author: Nicola Ricciardi
    """

    eventbus: EventBus
    connected: bool = field(default=False)

    async def connect(self):
        await super().connect()
        logging.info(f"subscriber {self.identifier} connecting...")
        self.connected = True

    async def disconnect(self):
        logging.info(f"subscriber {self.identifier} disconnecting...")
        self.connected = False

    async def _internal_subscribe(self, topic: str, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.add_subscriber(topic, self)

    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.remove_subscriber(self, topic)
