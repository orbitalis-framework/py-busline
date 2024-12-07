from typing import Callable
from busline.event.event import Event
from busline.local_client.eventbus.eventbus import EventBus
from busline.client.subscriber.listener.closure_event_handler import ClosureEventHandler
from busline.local_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalEventBusClosureSubscriber(ClosureEventHandler, LocalEventBusSubscriber):
    """
    Subscriber which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    def __init__(self, on_event_callback: Callable[[str, Event], None], subscriber_id: str | None = None, eventbus_instance: EventBus | None = None):
        super().__init__(subscriber_id=subscriber_id, eventbus_instance=eventbus_instance, on_event_callback=on_event_callback)