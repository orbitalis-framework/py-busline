import asyncio
from dataclasses import dataclass
from typing import Optional

from busline.client.client import EventBusClient
from busline.client.publisher.publisher import Publisher
from busline.event.event import Event
from busline.client.subscriber.subscriber import Subscriber


@dataclass
class PubSubClient(EventBusClient):
    """
    Eventbus client which should used by components which wouldn't be a publisher/subscriber, but they need them

    Author: Nicola Ricciardi
    """

    publisher: Publisher
    subscriber: Subscriber

    async def connect(self):
        await asyncio.gather(
            self.subscriber.connect(),
            self.publisher.connect()
        )

    async def disconnect(self):
        await asyncio.gather(
            self.subscriber.disconnect(),
            self.publisher.disconnect()
        )

    async def publish(self, topic: str, event: Event, **kwargs):
        """
        Alias of `client.publisher.publish(...)`
        """

        await self.publisher.publish(topic, event, **kwargs)

    async def subscribe(self, topic: str, **kwargs):
        """
        Alias of `client.subscriber.subscribe(...)`
        """

        await self.subscriber.subscribe(topic, **kwargs)

    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Alias of `client.subscriber.unsubscribe(...)`
        """

        await self.subscriber.unsubscribe(topic, **kwargs)
