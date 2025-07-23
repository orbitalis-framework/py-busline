import asyncio
import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, override, Optional

from busline.event.event import Event, RegistryPassthroughEvent
from busline.client.eventbus_connector import EventBusConnector
from busline.event.message.message import Message
from busline.event.message.number_message import Int64Message, Float64Message
from busline.event.message.string_message import StringMessage


class PublishMixin(ABC):

    @abstractmethod
    async def publish(self, topic: str, event: Event, **kwargs):
        raise NotImplemented()

    async def multi_publish(self, topics: List[str], event: Event, /, parallelize: bool = True, **kwargs):
        """
        Publish the same event in more topics
        """

        logging.debug(f"{self}: publish event {event} in {len(topics)} topics (parallelization: {parallelize})")

        if parallelize:
            tasks = [self.publish(topic, event, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.publish(topic, event, **kwargs)



@dataclass(eq=False)
class Publisher(EventBusConnector, PublishMixin, ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish messages

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
    async def publish(self, topic: str, message: Optional[Message | str | int | float] = None,
                      *, event_timestamp: Optional[datetime] = None, event_identifier: Optional[str] = None, **kwargs) -> Event:
        """
        Publish on topic the message and return the generated event.

        If str, int or float are used, the message is wrapper in StringMessage, Int64Message or Float64Message.

        Event use datetime.now() for timestamp and uuid4() for identifier by default.
        """

        if message is not None:
            if isinstance(message, str):
                message = StringMessage(message)

            if isinstance(message, int):
                message = Int64Message(message)

            if isinstance(message, float):
                message = Float64Message(message)

        if event_timestamp is None:
            event_identifier = datetime.now()

        if event_identifier is None:
            event_identifier = str(uuid.uuid4())

        event = Event(
            payload=message,
            identifier=event_identifier,
            timestamp=event_identifier,
            publisher_identifier=self.identifier
        )

        logging.info(f"{self}: publish on {topic} -> {event}")
        await self._on_publishing(topic, event, **kwargs)
        await self._internal_publish(topic, event, **kwargs)
        await self._on_published(topic, event, **kwargs)

        return event


    async def _on_publishing(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing start
        """

    async def _on_published(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing end
        """