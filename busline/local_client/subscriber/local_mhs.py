from typing import Callable

from busline.client.subscriber.listener.event_handler import EventHandler
from busline.client.subscriber.mhs import MultiHandlersSubscriber
from busline.event.event import Event
from busline.local_client.eventbus.eventbus import EventBus
from busline.local_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalMultiHandlersSubscriber(LocalEventBusSubscriber, MultiHandlersSubscriber):
    def __init__(self, subscriber_id: str | None = None, default_event_handler: EventHandler | Callable[[str, Event], None] | None = None, eventbus_instance: EventBus | None = None):
        LocalEventBusSubscriber.__init__(self, eventbus_instance)
        MultiHandlersSubscriber.__init__(self, subscriber_id, default_event_handler)
