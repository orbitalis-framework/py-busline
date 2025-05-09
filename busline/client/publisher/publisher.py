import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from busline.event.event import Event
from busline.client.eventbus_connector import EventBusConnector


@dataclass
class Publisher(EventBusConnector, ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish on eventbus

    Author: Nicola Ricciardi
    """

    def __repr__(self) -> str:
        return f"Publisher({self.identifier})"

    @abstractmethod
    async def _internal_publish(self, topic: str, event: Event, **kwargs):
        """
        Actual publish on topic the event

        :param topic:
        :param event:
        :return:
        """

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