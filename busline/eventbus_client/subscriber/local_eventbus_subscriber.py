from abc import ABC
from busline.eventbus.eventbus import EventBus
from busline.eventbus_client.exceptions import EventBusClientNotConnected
from busline.eventbus_client.subscriber.subscriber import Subscriber


class LocalEventBusSubscriber(Subscriber, ABC):
    """
    Abstract subscriber which works with local eventbus without implementing `on_event` method

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus):
        Subscriber.__init__(self)

        self._eventbus = eventbus_instance
        self._connected = False

    async def connect(self):
        self._connected = True

    async def disconnect(self):
        self._connected = False

    async def _internal_subscribe(self, topic_name: str, raise_if_not_connected: bool = False, **kwargs):
        if raise_if_not_connected and not self._connected:
            raise EventBusClientNotConnected()
        else:
            await self.connect()

        self._eventbus.add_subscriber(topic_name, self)

    async def _internal_unsubscribe(self, topic_name: str | None = None, raise_if_not_connected: bool = False, **kwargs):
        if raise_if_not_connected and not self._connected:
            raise EventBusClientNotConnected()
        else:
            await self.connect()

        self._eventbus.remove_subscriber(self, topic_name)