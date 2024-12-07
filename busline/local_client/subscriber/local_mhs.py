from typing import Callable

from busline.client.subscriber.listener.event_handler import EventHandler
from busline.client.subscriber.mhs import MultiHandlersSubscriber
from busline.event.event import Event
from busline.local_client.eventbus.eventbus import EventBus
from busline.local_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalMultiHandlersSubscriber(LocalEventBusSubscriber, MultiHandlersSubscriber):
    def __init__(self, subscriber_id: str | None = None, default_event_handler: EventHandler | Callable[[str, Event], None] | None = None, eventbus_instance: EventBus | None = None):
        super().__init__(subscriber_id, eventbus_instance=eventbus_instance, default_event_handler=default_event_handler)
