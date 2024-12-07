from uuid import uuid4
from busline.event.event import Event
from busline.client.publisher.publisher import Publisher
from busline.client.subscriber.subscriber import Subscriber


class EventBusClient:
    """
    Eventbus client which should used by components which wouldn't be a publisher/subscriber, but they need them

    Author: Nicola Ricciardi
    """

    def __init__(self, publisher: Publisher, subscriber: Subscriber):

        self.__publisher: Publisher = None
        self.__subscriber: Subscriber = None

        self.publisher = publisher
        self.subscriber = subscriber

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
        self.__subscriber = subscriber

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



