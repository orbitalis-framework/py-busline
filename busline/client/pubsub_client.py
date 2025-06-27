import asyncio
from dataclasses import dataclass, field
from typing import Optional, override, List, Self

from busline.client.client import EventBusClient
from busline.client.publisher.publisher import Publisher
from busline.client.subscriber.event_handler.event_handler import EventHandler
from busline.client.subscriber.topic_subscriber import TopicSubscriber
from busline.event.event import Event
from busline.client.subscriber.subscriber import Subscriber


@dataclass
class PubSubClient(EventBusClient):
    """
    Eventbus client which should used by components which wouldn't be a publisher/subscriber, but they need them

    Author: Nicola Ricciardi
    """

    publishers: List[Publisher]
    subscribers: List[Subscriber]

    @classmethod
    def from_pubsub(cls, publisher: Optional[Publisher] = None, subscriber: Optional[Subscriber] = None) -> Self:

        publishers = []
        if publisher is not None:
            publishers = [publisher]

        subscribers = []
        if subscriber is not None:
            subscribers = [subscriber]

        return cls(publishers, subscribers)

    @classmethod
    def from_pubsub_client(cls, client: Self) -> Self:
        return cls(client.publishers.copy(), client.subscribers.copy())

    @override
    async def connect(self):
        """
        Connect all publishers and subscribers
        """

        tasks = [publisher.connect() for publisher in self.publishers]
        tasks += [subscriber.connect() for subscriber in self.subscribers]

        await asyncio.gather(*tasks)

    @override
    async def disconnect(self):
        """
        Disconnect all publishers and subscribers
        """

        tasks = [publisher.disconnect() for publisher in self.publishers]
        tasks += [subscriber.disconnect() for subscriber in self.subscribers]

        await asyncio.gather(*tasks)

    @override
    async def publish(self, topic: str, event: Event, **kwargs):
        """
        Publish event using all publishers
        """

        await asyncio.gather(*[
            publisher.publish(topic, event, **kwargs) for publisher in self.publishers
        ])

    @override
    async def subscribe(self, topic: str, **kwargs):
        """
        Subscribe all subscribers on topic
        """

        await asyncio.gather(*[
            subscriber.subscribe(topic, **kwargs) for subscriber in self.subscribers
        ])

    @override
    async def unsubscribe(self, topic: Optional[str] = None, **kwargs):
        """
        Alias of `client.subscriber.unsubscribe(...)`
        """

        await asyncio.gather(*[
            subscriber.unsubscribe(topic, **kwargs) for subscriber in self.subscribers
        ])


@dataclass
class PubSubTopicClient(PubSubClient):
    """
    Eventbus client which should used by components which wouldn't be a publisher/subscriber, but they need them

    Author: Nicola Ricciardi
    """

    subscribers: List[TopicSubscriber]

    @override
    async def subscribe(self, topic: str, handler: Optional[EventHandler] = None, **kwargs):
        """
        Subscribe all subscribers on topic
        """

        await asyncio.gather(*[
            subscriber.subscribe(topic, handler=handler, **kwargs) for subscriber in self.subscribers
        ])


@dataclass
class PubSubClientBuilder:
    """
    Builder for a pub/sub client.

    Author: Nicola Ricciardi
    """

    base_client: PubSubClient = field(
        default_factory=lambda: PubSubClient([], []),
        kw_only=True
    )


    def with_publisher(self, publisher: Publisher) -> Self:
        self.base_client.publishers.append(publisher)

        return self

    def with_publishers(self, publishers: List[Publisher]) -> Self:
        self.base_client.publishers.extend(publishers)

        return self

    def with_subscriber(self, subscriber: Subscriber) -> Self:
        self.base_client.subscribers.append(subscriber)

        return self

    def with_subscribers(self, subscribers: List[Subscriber]) -> Self:
        self.base_client.subscribers.extend(subscribers)

        return self

    def build(self) -> PubSubClient:
        return self.base_client

