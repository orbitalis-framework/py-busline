from abc import ABC, abstractmethod
from dataclasses import dataclass
from busline.client.eventbus_connector import EventBusConnector
from busline.event.event import Event


@dataclass
class Subscriber(EventBusConnector, ABC):
    """
    Abstract class which can be implemented by your components which must be able to subscribe on eventbus

    Author: Nicola Ricciardi
    """

    @abstractmethod
    async def on_event(self, topic: str, event: Event):
        """
        Callback called when an event arrives from a topic
        """

    @abstractmethod
    async def _internal_subscribe(self, topic: str, **kwargs):
        """
        Actual subscribe to topic

        :param topic:
        :return:
        """

    @abstractmethod
    async def _internal_unsubscribe(self, topic: str | None = None, **kwargs):
        """
        Actual unsubscribe to topic

        :param topic:
        :return:
        """

    async def subscribe(self, topic: str, **kwargs):
        """
        Subscribe to topic

        :param topic:
        :return:
        """

        await self._on_subscribing(topic, **kwargs)
        await self._internal_subscribe(topic, **kwargs)
        await self._on_subscribed(topic, **kwargs)

    async def unsubscribe(self, topic: str | None = None, **kwargs):
        """
        Unsubscribe to topic

        :param topic:
        :return:
        """

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

    async def _on_unsubscribing(self, topic: str | None, **kwargs):
        """
        Callback called on unsubscribing

        :param topic:
        :return:
        """

    async def _on_unsubscribed(self, topic: str | None, **kwargs):
        """
        Callback called on unsubscribed

        :param topic:
        :return:
        """