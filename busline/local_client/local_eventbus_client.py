from typing import Callable
from uuid import uuid4

from busline.event.event import Event
from busline.local_client.eventbus.async_local_eventbus import AsyncLocalEventBus
from busline.client.eventbus_client import EventBusClient
from busline.local_client.eventbus.eventbus import EventBus
from busline.local_client.publisher.local_eventbus_publisher import LocalEventBusPublisher
from busline.local_client.subscriber.local_eventbus_closure_subscriber import LocalEventBusClosureSubscriber


class LocalEventBusClient(EventBusClient):

    def __init__(self, on_event_callback: Callable[[str, Event], None], client_id: str = str(uuid4()), eventbus_instance: EventBus | None = None):

        if eventbus_instance is None:
            eventbus_instance = AsyncLocalEventBus()

        EventBusClient.__init__(
            self,
            publisher=LocalEventBusPublisher(eventbus_instance=eventbus_instance),
            subscriber=LocalEventBusClosureSubscriber(on_event_callback, eventbus_instance=eventbus_instance),
            client_id=client_id
        )



