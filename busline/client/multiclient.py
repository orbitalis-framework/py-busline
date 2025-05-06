import asyncio
from dataclasses import dataclass
from typing import List, Optional

from busline.client.client import EventBusClient
from busline.event.event import Event


@dataclass
class EventBusMultiClient(EventBusClient):

    clients: List[EventBusClient]

    async def connect(self):
        tasks = [client.connect() for client in self.clients]
        await asyncio.gather(*tasks)

    async def disconnect(self):
        tasks = [client.disconnect() for client in self.clients]
        await asyncio.gather(*tasks)

    async def publish(self, topic: str, event: Event, **kwargs):
        tasks = [client.publish(topic, event) for client in self.clients]
        await asyncio.gather(*tasks)

    async def subscribe(self, topic: str, **kwargs):
        tasks = [client.subscribe(topic) for client in self.clients]
        await asyncio.gather(*tasks)

    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        tasks = [client.unsubscribe(topic) for client in self.clients]
        await asyncio.gather(*tasks)
