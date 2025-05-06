from typing import Callable, Optional
from dataclasses import dataclass

from busline.client.subscriber.event_handler.closure_event_handler import ClosureEventHandler
from busline.event.event import Event
from busline.client.pubsub_client import PubSubClient
from busline.local.eventbus.eventbus import EventBus
from busline.local.eventbus.local_eventbus import LocalEventBus
from busline.local.publisher.local_publisher import LocalEventBusPublisher
from busline.local.subscriber.local_subscriber import LocalEventBusMultiHandlersSubscriber


@dataclass
class LocalPubSubClient(PubSubClient):

    @staticmethod
    def from_callback(callback: Callable[[str, Event], None], eventbus: Optional[EventBus] = None) -> 'LocalPubSubClient':

        if eventbus is None:
            eventbus = LocalEventBus()

        return LocalPubSubClient(
            LocalEventBusPublisher(eventbus=eventbus),
            LocalEventBusMultiHandlersSubscriber(
                eventbus=eventbus,
                fallback_event_handler=ClosureEventHandler(callback)
            )
        )
