from abc import ABC, abstractmethod
from typing import Optional

from busline.event.event import Event


class EventBusClient(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def publish(self, topic: str, event: Event, **kwargs):
        pass

    @abstractmethod
    async def subscribe(self, topic: str, **kwargs):
        pass

    @abstractmethod
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        pass
