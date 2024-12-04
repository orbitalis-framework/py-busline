import logging
from abc import ABC, abstractmethod
from uuid import uuid4

from busline.event.event import Event
from busline.eventbus_client.eventbus_connector import EventBusConnector


class Publisher(EventBusConnector, ABC):
    """
    Abstract class which can be implemented by your components which must be able to publish on eventbus

    Author: Nicola Ricciardi
    """

    def __init__(self, publisher_id: str = str(uuid4())):
        EventBusConnector.__init__(self, publisher_id)

    @abstractmethod
    async def _internal_publish(self, topic_name: str, event: Event, **kwargs):
        """
        Actual publish on topic the event

        :param topic_name:
        :param event:
        :return:
        """

    async def publish(self, topic_name: str, event: Event, **kwargs):
        """
        Publish on topic the event

        :param topic_name:
        :param event:
        :return:
        """

        logging.debug(f"{self._id} publishing on {topic_name}: {event}")
        self.on_publishing(topic_name, event)
        await self._internal_publish(topic_name, event, **kwargs)
        self.on_published(topic_name, event)

    def on_publishing(self, topic_name: str, event: Event):
        """
        Callback called on publishing start

        :param topic_name:
        :param event:
        :return:
        """

    def on_published(self, topic_name: str, event: Event):
        """
        Callback called on publishing end

        :param topic_name:
        :param event:
        :return:
        """