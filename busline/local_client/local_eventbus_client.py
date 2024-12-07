from typing import Callable
from uuid import uuid4

from busline.event.event import Event
from busline.local_client import DEFAULT_EVENT_BUS_INSTANCE
from busline.local_client.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.client.eventbus_client import EventBusClient
from busline.local_client.eventbus.eventbus import EventBus
from busline.local_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.local_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber


class LocalEventBusClient(EventBusClient):

    def __init__(self, on_event_callback: Callable[[str, Event], None], client_id: str = str(uuid4()), eventbus_instance: EventBus | None = None):

        if eventbus_instance is None:
            eventbus_instance = DEFAULT_EVENT_BUS_INSTANCE

        EventBusClient.__init__(
            self,
            publisher=LocalEventBusPublisher(publisher_id=client_id, eventbus_instance=eventbus_instance),
            subscriber=LocalEventBusClosureSubscriber(subscriber_id=client_id, on_event_callback=on_event_callback, eventbus_instance=eventbus_instance),
        )



