import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, override

from busline.event.event import Event
from busline.client.eventbus_connector import EventBusConnector


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

        :param topic:
        :param event:
        :return:
        """

    @override
    async def publish(self, topic: str, event: Event, **kwargs):
        """
        Publish on topic the event

        :param topic:
        :param event:
        :return:
        """

        logging.info(f"{self}: publish on {topic} -> {event}")
        await self.on_publishing(topic, event, **kwargs)
        await self._internal_publish(topic, event, **kwargs)
        await self.on_published(topic, event, **kwargs)


    async def on_publishing(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing start

        :param topic:
        :param event:
        :return:
        """

    async def on_published(self, topic: str, event: Event, **kwargs):
        """
        Callback called on publishing end

        :param topic:
        :param event:
        :return:
        """