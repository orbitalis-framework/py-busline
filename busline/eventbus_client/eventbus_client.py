from uuid import uuid4
from busline.event.event import Event
from busline.eventbus_client.eventbus_connector import EventBusConnector
from busline.eventbus_client.publisher.publisher import Publisher
from busline.eventbus_client.subscriber.event_listener import EventListener
from busline.eventbus_client.subscriber.subscriber import Subscriber


class EventBusClient(EventBusConnector):
    """
    Eventbus client which should used by components which wouldn't be a publisher/subscriber, but they need them

    Author: Nicola Ricciardi
    """

    def __init__(self, publisher: Publisher, subscriber: Subscriber, event_listener: EventListener | None = None, client_id: str = str(uuid4())):
        EventBusConnector.__init__(self, client_id)

        self._id = client_id
        self.__publisher: Publisher = None
        self.__subscriber: Subscriber = None
        self.__event_listener: EventListener = None

        self.publisher = publisher
        self.subscriber = subscriber
        self.event_listener = event_listener

    @property
    def publisher(self) -> Publisher:
        return self.__publisher

    @publisher.setter
    def publisher(self, publisher: Publisher):
        self.__publisher = publisher

    @property
    def subscriber(self) -> Subscriber:
        return self.__subscriber

    @subscriber.setter
    def subscriber(self, subscriber: Subscriber):

        original_on_event = subscriber.on_event

        async def on_event_wrapper(*args, **kwargs):        # wrap on_event method to call self.on_event
            await original_on_event(*args, **kwargs)
            await self.on_event(*args, **kwargs)

        subscriber.on_event = on_event_wrapper
        self.__subscriber = subscriber

    @property
    def event_listener(self) -> EventListener:
        return self.__event_listener

    @event_listener.setter
    def event_listener(self, event_listener: EventListener):
        self.__event_listener = event_listener

    async def connect(self):
        c1 = self.__publisher.connect()
        c2 = self.__subscriber.connect()

        await c1
        await c2

    async def disconnect(self):
        d1 = self.__publisher.disconnect()
        d2 = self.__subscriber.disconnect()

        await d1
        await d2

    async def publish(self, topic_name: str, event: Event, **kwargs):
        """
        Alias of `client.publisher.publish(...)`
        """

        await self.__publisher.publish(topic_name, event, **kwargs)

    async def subscribe(self, topic_name: str, **kwargs):
        """
        Alias of `client.subscriber.subscribe(...)`
        """

        await self.__subscriber.subscribe(topic_name, **kwargs)

    async def unsubscribe(self, topic_name: str | None = None, **kwargs):
        """
        Alias of `client.subscriber.unsubscribe(...)`
        """

        await self.__subscriber.unsubscribe(topic_name, **kwargs)

    async def on_event(self, topic_name: str, event: Event, **kwargs):
        if self.__event_listener is not None:
            await self.__event_listener.on_event(topic_name, event, **kwargs)


