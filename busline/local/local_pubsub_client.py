from typing import Callable, Self, override, Optional
from dataclasses import dataclass, field
from busline.client.subscriber.topic_subscriber.event_handler.callback_event_handler import CallbackEventHandler
from busline.event.event import Event
from busline.client.pubsub_client import PubSubClient, PubSubClientBuilder, PubTopicSubClient, PubTopicSubClientBuilder
from busline.local.eventbus.eventbus import EventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.local.subscriber.local_subscriber import LocalEventBusSubscriber


@dataclass
class LocalPubTopicSubClientBuilder(PubTopicSubClientBuilder):
    """
    Builder for a local pub/sub client.

    EventBus fed in init will be used to build publishers and subscribers

    Author: Nicola Ricciardi
    """

    @classmethod
    def default(cls, *, eventbus: Optional[LocalEventBus] = None) -> PubTopicSubClient:

        if eventbus is None:
            eventbus = LocalEventBus()

        return (cls()
                .with_subscriber(LocalEventBusSubscriber(eventbus=eventbus))
                .with_publisher(LocalEventBusPublisher(eventbus=eventbus))
                .build())

