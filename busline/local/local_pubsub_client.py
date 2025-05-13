from typing import Callable, Optional, Self, override
from dataclasses import dataclass, field
from busline.client.publisher.publisher import Publisher
from busline.client.subscriber.event_handler.closure_event_handler import ClosureEventHandler
from busline.event.event import Event
from busline.client.pubsub_client import PubSubClient, PubSubClientBuilder
from busline.local.eventbus.eventbus import EventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.local.subscriber.local_subscriber import LocalEventBusSubscriber


@dataclass
class LocalPubSubClient(PubSubClient):
    pass


@dataclass
class LocalPubSubClientBuilder(PubSubClientBuilder):
    """
    Builder for a local pub/sub client.

    EventBus fed in init will be used to build publishers and subscribers

    Author: Nicola Ricciardi
    """

    eventbus: EventBus = field(default_factory=LocalEventBus)

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
                fallback_event_handler=ClosureEventHandler(closure)
            )
        )

        return self

    @override
    def build(self) -> LocalPubSubClient:
        return LocalPubSubClient.from_pubsub_client(self.base_client)

