import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, override, Optional

from busline.event.event import Event, RegistryBasedEvent
from busline.client.eventbus_connector import EventBusConnector
from busline.event.message import Message


class PublishMixin(ABC):

    @abstractmethod
    async def publish(self, topic: str, event: Event, **kwargs):
        raise NotImplemented()

    async def multi_publish(self, topics: List[str], event: Event, /, parallelize: bool = True, **kwargs):
        """
        Publish the same event in more topics
        """

        logging.debug(f"{self}: publish event {event.identifier} in {len(topics)} topics (parallelization: {parallelize})")

        if parallelize:
            tasks = [self.publish(topic, event, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.publish(topic, event, **kwargs)



@dataclass(eq=False)
class Publisher(EventBusConnector, PublishMixin, ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish on eventbus

    Author: Nicola Ricciardi
    """

    def __str__(self) -> str:
        return f"Publisher('{self.identifier}')"

    @abstractmethod
    async def _internal_publish(self, topic: str, event: Event, **kwargs):
        """
        Actual publish on topic the event
        """

    @override
    async def publish(self, topic: str, message: Optional[Message] = None, **kwargs) -> Event:
        """
        Publish on topic the message and return the generated event
        """

        event = Event(
            payload=message,
            identifier=str(uuid.uuid4()),
            timestamp=datetime.now(),
            publisher_identifier=self.identifier
        )

        logging.info(f"{self}: publish on {topic} -> {event}")
        await self.on_publishing(topic, event, **kwargs)
        await self._internal_publish(topic, event, **kwargs)
        await self.on_published(topic, event, **kwargs)

        return event


    async def on_publishing(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing start
        """

    async def on_published(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing end
        """