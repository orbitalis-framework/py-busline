from typing import Callable, Self, override
from dataclasses import dataclass, field
from busline.client.subscriber.topic_subscriber.event_handler.callback_event_handler import CallbackEventHandler
from busline.event.event import Event
from busline.client.pubsub_client import PubSubClient, PubSubClientBuilder, PubTopicSubClient
from busline.local.eventbus.eventbus import EventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.local.subscriber.local_subscriber import LocalEventBusSubscriber


@dataclass
class LocalPubSubClient(PubSubClient):
    pass


@dataclass
class LocalPubTopicSubClient(PubTopicSubClient):
    pass


@dataclass
class LocalPubSubClientBuilder(PubSubClientBuilder):
    """
    Builder for a local pub/sub client.

    EventBus fed in init will be used to build publishers and subscribers

    Author: Nicola Ricciardi
    """

    eventbus: EventBus = field(default_factory=LocalEventBus)
    base_client: LocalPubSubClient = field(
        default_factory=lambda: LocalPubSubClient([], []),
        kw_only=True
    )

    def with_default_publisher(self) -> Self:
        """"
        LocalEventBusPublisher coupled with eventbus is used
        """

        self.base_client.publishers.append(
            LocalEventBusPublisher(eventbus=self.eventbus)
        )

        return self

    def with_closure_subscriber(self, closure: Callable[[str, Event], None]) -> Self:
        self.base_client.subscribers.append(
            LocalEventBusSubscriber(
                eventbus=self.eventbus,
                fallback_event_handler=CallbackEventHandler(closure)
            )
        )

        return self

    @override
    def build(self) -> LocalPubSubClient:
        return LocalPubSubClient.from_pubsub_client(self.base_client)


@dataclass
class LocalPubTopicSubClientBuilder(PubSubClientBuilder):
    """
    Builder for a local pub/sub client.

    EventBus fed in init will be used to build publishers and subscribers

    Author: Nicola Ricciardi
    """

    eventbus: EventBus = field(default_factory=LocalEventBus)
    base_client: LocalPubTopicSubClient = field(
        default_factory=lambda: LocalPubTopicSubClient([], []),
        kw_only=True
    )

    def with_default_publisher(self) -> Self:
        """"
        LocalEventBusPublisher coupled with eventbus is used
        """

        self.base_client.publishers.append(
            LocalEventBusPublisher(eventbus=self.eventbus)
        )

        return self

    def with_closure_subscriber(self, closure: Callable[[str, Event], None]) -> Self:
        self.base_client.subscribers.append(
            LocalEventBusSubscriber(
                eventbus=self.eventbus,
                fallback_event_handler=CallbackEventHandler(closure)
            )
        )

        return self

    @override
    def build(self) -> LocalPubTopicSubClient:
        return LocalPubTopicSubClient.from_pubsub_client(self.base_client)