from abc import ABC, abstractmethod
from uuid import uuid4

from busline.event.event import Event
from busline.eventbus_client.eventbus_connector import EventBusConnector
from busline.eventbus_client.subscriber.event_listener import EventListener


class Subscriber(EventBusConnector, EventListener, ABC):
    """
    Abstract class which can be implemented by your components which must be able to subscribe on eventbus

    Author: Nicola Ricciardi
    """

    def __init__(self, subscriber_id: str = str(uuid4())):
        EventBusConnector.__init__(self, subscriber_id)
        EventListener.__init__(self)


    @abstractmethod
    async def _internal_subscribe(self, topic_name: str, **kwargs):
        """
        Actual subscribe to topic

        :param topic_name:
        :return:
        """

    @abstractmethod
    async def _internal_unsubscribe(self, topic_name: str | None = None, **kwargs):
        """
        Actual unsubscribe to topic

        :param topic_name:
        :return:
        """

    async def subscribe(self, topic_name: str, **kwargs):
        """
        Subscribe to topic

        :param topic_name:
        :return:
        """

        self.on_subscribing(topic_name)
        await self._internal_subscribe(topic_name, **kwargs)
        self.on_subscribed(topic_name)

    async def unsubscribe(self, topic_name: str | None = None, **kwargs):
        """
        Unsubscribe to topic

        :param topic_name:
        :return:
        """

        self.on_unsubscribing(topic_name)
        await self._internal_unsubscribe(topic_name, **kwargs)
        self.on_unsubscribed(topic_name)

    def on_subscribing(self, topic_name: str):
        """
        Callback called on subscribing

        :param topic_name:
        :return:
        """

    def on_subscribed(self, topic_name: str):
        """
        Callback called on subscribed

        :param topic_name:
        :return:
        """

    def on_unsubscribing(self, topic_name: str):
        """
        Callback called on unsubscribing

        :param topic_name:
        :return:
        """

    def on_unsubscribed(self, topic_name: str):
        """
        Callback called on unsubscribed

        :param topic_name:
        :return:
        """