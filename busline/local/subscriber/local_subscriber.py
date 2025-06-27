import logging
from dataclasses import dataclass, field
from typing import Optional, override

from busline.client.subscriber.topic_subscriber import TopicSubscriber
from busline.local.eventbus.eventbus import EventBus
from busline.exceptions import EventBusClientNotConnected


ALL_TOPIC_WILDCARD = "*"


@dataclass
class LocalEventBusSubscriber(TopicSubscriber):
    """
    Subscriber topic-based which works with local eventbus

    Author: Nicola Ricciardi
    """

    eventbus: EventBus
    connected: bool = field(default=False)

    @override
    async def connect(self):
        logging.info(f"subscriber {self.identifier} connecting...")
        self.connected = True

    @override
    async def disconnect(self):
        logging.info(f"subscriber {self.identifier} disconnecting...")
        self.connected = False

    @override
    async def _internal_subscribe(self, topic: str, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.add_subscriber(topic, self)

    @override
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        if not self.connected:
            raise EventBusClientNotConnected()

        self.eventbus.remove_subscriber(self, topic)
