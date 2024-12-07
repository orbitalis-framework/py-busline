import logging
from abc import ABC, abstractmethod
from uuid import uuid4

from busline.event.event import Event
from busline.client.eventbus_connector import EventBusConnector


class Publisher(EventBusConnector, ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish on eventbus

    Author: Nicola Ricciardi
    """

    def __init__(self, publisher_id: str | None = None):
        
        if publisher_id is None:
            publisher_id = str(uuid4())
        
        super().__init__(publisher_id)

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

        logging.debug(f"{self._id} publishing on {topic}: {event}")
        await self.on_publishing(topic, event)
        await self._internal_publish(topic, event, **kwargs)
        await self.on_published(topic, event)

    async def on_publishing(self, topic: str, event: Event):
        """
        Callback called on publishing start

        :param topic:
        :param event:
        :return:
        """

    async def on_published(self, topic: str, event: Event):
        """
        Callback called on publishing end

        :param topic:
        :param event:
        :return:
        """