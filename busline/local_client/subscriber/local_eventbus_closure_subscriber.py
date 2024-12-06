from typing import Callable
from busline.event.event import Event
from busline.local_client.eventbus.eventbus import EventBus
from busline.client.subscriber.closure_event_listener import ClosureEventListener
from busline.local_client.subscriber.local_eventbus_subscriber import LocalEventBusSubscriber


class LocalEventBusClosureSubscriber(LocalEventBusSubscriber, ClosureEventListener):
    """
    Subscriber which works with local eventbus, this class can be initialized and used stand-alone

    Author: Nicola Ricciardi
    """

    def __init__(self, on_event_callback: Callable[[str, Event], None], eventbus_instance: EventBus | None = None):
        LocalEventBusSubscriber.__init__(self, eventbus_instance)
        ClosureEventListener.__init__(self, on_event_callback)