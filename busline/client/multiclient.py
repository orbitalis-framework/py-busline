import asyncio
from dataclasses import dataclass
from typing import List, Optional, override

from busline.client.client import EventBusClient
from busline.event.event import Event


@dataclass
class EventBusMultiClient(EventBusClient):

    clients: List[EventBusClient]

    @classmethod
    def from_client(cls, client: EventBusClient):
        return cls([client])

    @override
    async def connect(self):
        tasks = [client.connect() for client in self.clients]
        await asyncio.gather(*tasks)

    @override
    async def disconnect(self):
        tasks = [client.disconnect() for client in self.clients]
        await asyncio.gather(*tasks)

    @override
    async def publish(self, topic: str, event: Event, **kwargs):
        tasks = [client.publish(topic, event, **kwargs) for client in self.clients]
        await asyncio.gather(*tasks)

    @override
    async def subscribe(self, topic: str, **kwargs):
        tasks = [client.subscribe(topic, **kwargs) for client in self.clients]
        await asyncio.gather(*tasks)

    @override
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        tasks = [client.unsubscribe(topic, **kwargs) for client in self.clients]
        await asyncio.gather(*tasks)
