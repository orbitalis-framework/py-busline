import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, override, List

from busline.client.eventbus_connector import EventBusConnector
from busline.event.event import Event


class SubscribeMixin(ABC):
    @abstractmethod
    async def subscribe(self, topic: str, **kwargs):
        raise NotImplemented()

    async def multi_subscribe(self, topics: List[str], /, parallelize: bool = True, **kwargs):
        logging.debug(f"{self}: subscribe to {len(topics)} topics (parallelization: {parallelize})")

        if parallelize:
            tasks = [self.subscribe(topic, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.subscribe(topic, **kwargs)

    @abstractmethod
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        raise NotImplemented()

    async def multi_unsubscribe(self, topics: List[str], /, parallelize: bool = True, **kwargs):
        logging.debug(f"{self}: unsubscribe from {len(topics)} topics (parallelization: {parallelize})")

        if parallelize:
            tasks = [self.unsubscribe(topic, **kwargs) for topic in topics]
            await asyncio.gather(*tasks)

        else:
            for topic in topics:
                await self.unsubscribe(topic, **kwargs)



@dataclass(eq=False)
class Subscriber(EventBusConnector, SubscribeMixin, ABC):
    """
    Abstract class which can be implemented by your components which must be able to subscribe on eventbus

    Author: Nicola Ricciardi
    """

    def __str__(self) -> str:
        return f"Subscriber('{self.identifier}')"

    @abstractmethod
    async def on_event(self, topic: str, event: Event):
        """
        Callback called when an event arrives from a topic
        """

    async def notify(self, topic: str, event: Event, **kwargs):
        """
        Notify subscriber
        """

        logging.info(f"{self}: incoming event on {topic} -> {event}")
        await self.on_event(topic, event)

    @abstractmethod
    async def _internal_subscribe(self, topic: str, **kwargs):
        """
        Actual subscribe to topic

        :param topic:
        :return:
        """

    @abstractmethod
    async def _internal_unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Actual unsubscribe to topic

        :param topic:
        :return:
        """

    @override
    async def subscribe(self, topic: str, **kwargs):
        """
        Subscribe to topic

        :param topic:
        :return:
        """

        logging.info(f"{self}: subscribe on topic {topic}")
        await self._on_subscribing(topic, **kwargs)
        await self._internal_subscribe(topic, **kwargs)
        await self._on_subscribed(topic, **kwargs)

    @override
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Unsubscribe to topic

        :param topic:
        :return:
        """

        logging.info(f"{self}: unsubscribe from topic {topic}")
        await self._on_unsubscribing(topic, **kwargs)
        await self._internal_unsubscribe(topic, **kwargs)
        await self._on_unsubscribed(topic, **kwargs)

    async def _on_subscribing(self, topic: str, **kwargs):
        """
        Callback called on subscribing

        :param topic:
        :return:
        """

    async def _on_subscribed(self, topic: str, **kwargs):
        """
        Callback called on subscribed

        :param topic:
        :return:
        """

    async def _on_unsubscribing(self, topic: Optional[str], **kwargs):
        """
        Callback called on unsubscribing

        :param topic:
        :return:
        """

    async def _on_unsubscribed(self, topic: Optional[str], **kwargs):
        """
        Callback called on unsubscribed

        :param topic:
        :return:
        """