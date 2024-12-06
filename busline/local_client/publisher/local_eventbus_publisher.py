from busline.event.event import Event
from busline.local_client import DEFAULT_EVENT_BUS_INSTANCE
from busline.local_client.eventbus.eventbus import EventBus
from busline.client.exceptions import EventBusClientNotConnected
from busline.client.publisher.publisher import Publisher


class LocalEventBusPublisher(Publisher):
    """
    Publisher which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    def __init__(self, eventbus_instance: EventBus | None = None):
        Publisher.__init__(self)

        if eventbus_instance is None:
            eventbus_instance = DEFAULT_EVENT_BUS_INSTANCE

        self._eventbus = eventbus_instance
        self._connected = False

    async def connect(self):
        self._connected = True

    async def disconnect(self):
        self._connected = False

    async def _internal_publish(self, topic_name: str, event: Event, raise_if_not_connected: bool = False, **kwargs):

        if raise_if_not_connected and not self._connected:
            raise EventBusClientNotConnected()
        else:
            await self.connect()

        self.on_publishing(topic_name, event)
        await self._eventbus.put_event(topic_name, event)
        self.on_published(topic_name, event)